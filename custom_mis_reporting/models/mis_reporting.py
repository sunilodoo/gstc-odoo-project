# -*- coding: utf-8 -*-
from odoo import models, fields, osv, api, _
from odoo.tools.translate import _
from odoo.exceptions import Warning
import datetime
USER_PRIVATE_FIELDS = ['password']

class MisReporting(models.Model):
	_inherit = 'mail.thread'
	_name = 'mis.reporting'
	_order = "target asc"

	@api.depends('target','execute','production')
	def calc_all(self):
		target_byday = 0.0
		execute_byday = 0.0
		ach_per = 0.0
		ttl_ach_per = 0.0
		month_unit = 0.0
		total_sale = 0.0
		dic = {'Apr':1, 'May':2, 'Jun':3, 'Jul':4, 'Aug':5, 'Sep':6, 'Oct':7, 'Nov':8, 'Dec':9, 'Jan':10, 'Feb':11, 'Mar':12}
		#fin_day = datetime.date(2017, 04, 01)
		#today = datetime.date.today()
		#diff = today - fin_day
		for rec in self:
			#if rec.inv_id:
			#	rec.execute = sum(inv.amount for inv in rec.inv_id)
			if rec.target > 0 :
				target_byday = (rec.target / 12 )*dic[datetime.datetime.today().strftime('%b')]
				rec.target_byday = target_byday
			if rec.execute > 0 :
				execute_byday = rec.execute / dic[datetime.datetime.today().strftime('%b')]
				rec.execute_byday = execute_byday
				month_unit = rec.execute / dic[datetime.datetime.today().strftime('%b')]
				rec.month_unit = month_unit
			if rec.target_byday > 0 and rec.execute > 0 :
				ach_per = (rec.execute * 100)/rec.target_byday
				rec.acheive = ach_per
			if (rec.execute > 0 or rec.production > 0) and rec.target > 0:
				#ttl_ach_per = (rec.execute + rec.production)*100/rec.target_byday
				ttl_ach_per = (rec.execute + rec.production)*100/(rec.target_byday + 60)
				rec.total_acheive = ttl_ach_per
			rec.total_sale = rec.execute + rec.production
			
			# print"--------------======-------",rec.target,rec.target_byday,rec.month
	
	name = fields.Many2one('hr.employee', string='Coordinator')
	proc_name = fields.Many2one('hr.employee', string='Procu. Coordinator')
	salary = fields.Float('Salary')
	order_id = fields.Many2one('sale.order', 'SO No.')
	country = fields.Many2one('res.country', 'Country')
	buyer = fields.Many2one('res.partner', string='Buyer')
	region = fields.Many2one('res.region', string='Region')
	target = fields.Float('Target')
	target_year = fields.Many2one('fin.year', string='Financial Year', default=5)
	#inv_id = fields.One2many('inv.details', 'i_id', string='Invoice')
	invoice = fields.Char('Invoice Number')
	production = fields.Float('Confirmed SO')
	month = fields.Selection([('jan', 'January'), ('feb', 'February'), ('mar', 'March'), ('apr', 'April'), ('may', 'May'), ('jun', 'June'), ('jul', 'July'), ('aug', 'August'), ('sept', 'September'), ('oct', 'October'), ('nov', 'November'), ('dec', 'December')], string='Dispatch Month')
	dispatch_date = fields.Date('Dispatch Date')
	month_unit = fields.Float('Sales/Month', compute='calc_all', track_visibility='always', store=True)
	pipeline = fields.Float(' Pipeline/ P.I Raised')
	remarks = fields.Text('Remarks')
	edd = fields.Date('Expected Date Dispatch')
	so_date = fields.Date('SO placed Date')
	days = fields.Integer('Days')
	execute = fields.Float('Executed FE($)')
	execute_inr = fields.Float('Executed INR(₹)')
	target_byday = fields.Float('Target/month Till date', compute='calc_all', track_visibility='always', store=True)
	execute_byday = fields.Float('Executed/month', compute='calc_all', track_visibility='always', store=True)
	acheive = fields.Float('Acheived executed (%)', compute='calc_all', track_visibility='always', store=True)
	total_acheive = fields.Float('Total (EC)Acheived (%)', compute='calc_all', track_visibility='always', store=True)
	total_sale = fields.Float('Total Sale(EC)', compute='calc_all', track_visibility='always', store=True)
	boolen_finance = fields.Boolean('Finance Boolean', default=True)

	md_id = fields.Many2one('res.users', default=8)
	md2_id = fields.Many2one('res.users', default=10)
	sale_year1_amount = fields.Float("Sale Year1")
	sale_year2_amount = fields.Float("Sale Year2")
	follow_up = fields.Text("Follow Up")
	category_id = fields.Many2many("res.partner.category", string="Tags")
	opportunity = fields.Float("Opportunity")


	@api.onchange('buyer')
	def change_country(self):
		# print"--------------======-------",self.buyer
		if not (self.buyer and self.buyer.country_id):
			raise Warning(_("Buyer's country not defined! "))
		if self.buyer and self.buyer.country_id:
			self.country = self.buyer.country_id.id

	@api.onchange('edd','so_date')
	def change_days(self):
		# print"--------------======-------",self.edd
		if self.edd and self.so_date:
			days = datetime.datetime.strptime(self.edd, '%Y-%m-%d') - datetime.datetime.strptime(self.so_date, '%Y-%m-%d')
			# print"--------------======----------",days.days
			self.days = days.days

	@api.onchange('invoice','dispatch_date')
	def sale_mark_days(self):
		sale_mark1= self.env['po_mis.reporting'].search([('po_no.id','=',self.order_id.id)])
		# print"------sale_mark1--------=-----",sale_mark1
		if sale_mark1:
			sale_mark1.write({'invoice': self.invoice,'invoice_date':self.dispatch_date})
			# print"1111111111111111111111111111"

	@api.multi
	def po_detalis(self):
		#po = self.env['purchase.order'].search([('origin', 'like', self.order_id.name)])
		l = []
		
		po = self.env['purchase.order'].search([('origin', 'like', self.order_id.name)])
		if not po:
			raise Warning(_("SO not Found! "))
		for p in po:
			#if not p.state in ['draft','sent']:
			p_mis = self.env['po_item.history'].search([('po_id', '=', p.id)])
			for pm in p_mis:
				l.append(pm.id)
		ids = [m for m in l]
		return {
			'name':   ('Summary Mkt.'),
			'view_type': 'form',
			'view_mode': 'tree,form',
			'res_model': 'po_item.history',
			'context':self._context,
			'domain':[('id','in',ids)],
			'type': 'ir.actions.act_window',
			'target': 'current',
			'flags': {'form': {'action_buttons': True}}
		}	
	
	@api.model
	def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
		result = super(MisReporting, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)
		if 'acheive' in fields:
			for rec in result:
				if rec['execute'] > 0 and rec['target_byday'] > 0:
					rec['acheive'] = (rec['execute'] * 100)/rec['target_byday']
		if 'total_acheive' in fields:
			for rec in result:
				if rec['execute'] > 0 and rec['execute'] > 0 and rec['target_byday'] > 0:
					rec['total_acheive'] = ((rec['execute'] + rec['production'])* 100)/rec['target_byday']
		return result

class SaleAdvancePaymentInv(models.TransientModel):
	_inherit="sale.advance.payment.inv"

	@api.multi
	def create_invoices(self):
		sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
		for rec in sale_orders:
			mis_report=self.env['mis.reporting'].search([('order_id.id','=',rec.id)])
			if mis_report:
				for i_mis in mis_report:
					i_mis.execute=i_mis.production
					i_mis.production=0
			# if mis_report:
			# 	mis_report.execute=mis_report.production
			# 	mis_report.production=0
		result = super(SaleAdvancePaymentInv, self).create_invoices()
		return result

class ResRegion(models.Model):
	_name = 'res.region'
	
	name = fields.Char(string='Name')

class finYear(models.Model):
	_name = 'fin.year'
	
	name = fields.Char(string='Name')

class ResPartner(models.Model):
	_inherit = 'res.partner'

	@api.multi
	def generate_sereis(self):
		# print"-----------------------"
		
		#print"target_id=========",target_id
		#self.target_value = target_id.id
		#print"target_id.name",target_id.name,self.target_value.name
		part = self.search([('active','=',True)])
		#print"partner_id",partner_id
		for partner in part:
			target_id = self.env['target.value'].search([('tr_id','=',partner.id)])
			print"partner-----------",partner
			partner.target_value = target_id.id

	target_value = fields.Many2one('target.value', string='Target')

class target_value(models.Model):
	_name='target.value'

	tr_id = fields.Many2one('res.partner', string='Customer')
	finance_yr = fields.Many2one('fin.year', string='Financial Year')
	sales_per = fields.Many2one('res.users', string='Sales Person')
	name = fields.Float('Target')
	pipe_line = fields.Float('Pipline')
	pro_duct = fields.Float('Production')
	executed = fields.Float('Executed')
	balance = fields.Float('Balance')

	@api.onchange('name','pipe_line','pro_duct','executed')
	def calc_diff(self):
		if self.name:
			self.balance = self.name - (self.pipe_line + self.pro_duct + self.executed)

'''
class InvDetails(models.Model):
	_name = 'inv.details'
	
	i_id = fields.Many2one('mis.reporting', 'ID')
	name = fields.Char(string='Invoice Number')
	amount = fields.Float('Amount')
	dispatch_date = fields.Date('Dispatch Date')
'''	
