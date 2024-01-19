# -*- coding: utf-8 -*-
from odoo import models, fields, osv, api, _
from odoo.tools.translate import _
from odoo.exceptions import Warning
import datetime

class MisReporting(models.Model):
	_name = 'mis.reporting'

	@api.depends('target','execute')
	def calc_all(self):
		target_byday = 0.0
		execute_byday = 0.0
		ach_per = 0.0
		ttl_ach_per = 0.0
		month_unit = 0.0
		dic = {'Apr':1, 'May':2, 'Jun':3, 'Jul':4, 'Aug':5, 'Sept':6, 'Oct':7, 'Nov':8, 'Dec':9, 'Jan':10, 'Feb':11, 'Mar':12}
		#fin_day = datetime.date(2017, 04, 01)
		#today = datetime.date.today()
		#diff = today - fin_day
		for rec in self:
			#if rec.inv_id:
			#	rec.execute = sum(inv.amount for inv in rec.inv_id)
			if rec.target > 0 and rec.execute > 0 :
				ach_per = (rec.execute * 100)/rec.target
				rec.acheive = ach_per
			if rec.target > 0 :
				target_byday = (rec.target / 12 )*dic[datetime.datetime.today().strftime('%b')]
				rec.target_byday = target_byday
			if rec.execute > 0 :
				execute_byday = rec.execute / dic[datetime.datetime.today().strftime('%b')]
				rec.execute_byday = execute_byday
				month_unit = rec.execute / dic[datetime.datetime.today().strftime('%b')]
				rec.month_unit = month_unit
			if (rec.execute > 0 or rec.production > 0) and rec.target > 0:
				ttl_ach_per = (rec.execute + rec.production)*100/rec.target
				rec.total_acheive = ttl_ach_per
			
			print"--------------======-------",rec.target,rec.target_byday,rec.month
	
	name = fields.Many2one('hr.employee', string='Coordinator')
	proc_name = fields.Many2one('hr.employee', string='Procu. Coordinator')
	salary = fields.Float('Salary')
	country = fields.Many2one('res.country', 'Country')
	buyer = fields.Many2one('res.partner', string='Buyer')
	region = fields.Many2one('res.region', string='Region')
	target = fields.Float('Target')
	target_year = fields.Many2one('fin.year', string='Financial Year')
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
	execute = fields.Float('Executed FE')
	execute_inr = fields.Float('Executed INR')
	target_byday = fields.Float('Target/month Till date', compute='calc_all', track_visibility='always', store=True)
	execute_byday = fields.Float('Executed/month', compute='calc_all', track_visibility='always', store=True)
	acheive = fields.Float('Acheived executed (%)', compute='calc_all', track_visibility='always', store=True)
	total_acheive = fields.Float('Total Acheived (%)', compute='calc_all', track_visibility='always', store=True)

	@api.onchange('buyer')
	def change_country(self):
		print"--------------======-------",self.buyer
		if not (self.buyer and self.buyer.country_id):
			raise Warning(_("Buyer's country not defined! "))
		if self.buyer and self.buyer.country_id:
			self.country = self.buyer.country_id.id

	@api.onchange('edd','so_date')
	def change_days(self):
		print"--------------======-------",self.edd
		if self.edd and self.so_date:
			days = datetime.datetime.strptime(self.edd, '%Y-%m-%d') - datetime.datetime.strptime(self.so_date, '%Y-%m-%d')
			print"--------------======----------",days.days
			self.days = days.days

	

class ResRegion(models.Model):
	_name = 'res.region'
	
	name = fields.Char(string='Name')

class finYear(models.Model):
	_name = 'fin.year'
	
	name = fields.Char(string='Name')
'''
class InvDetails(models.Model):
	_name = 'inv.details'
	
	i_id = fields.Many2one('mis.reporting', 'ID')
	name = fields.Char(string='Invoice Number')
	amount = fields.Float('Amount')
	dispatch_date = fields.Date('Dispatch Date')
'''	
