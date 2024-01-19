# -*- coding: utf-8 -*-

from odoo import models, fields, osv, api, _
from odoo.tools.translate import _
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import Warning, UserError
from datetime import timedelta
import datetime

class ProcurementPanel(models.Model):
	_name = "procurement.panel"
	#_order = 'date_invoice desc'

	name = fields.Char('PI (SO No.)')
	order_id = fields.Many2one('sale.order', string="PI (SO No.)")
	order_date = fields.Date("PI (SO Date)")
	partner_id = fields.Many2one("res.partner", string="Customer")	
	country_id = fields.Many2one('res.country', string='Country')
	company_id = fields.Many2one('res.company', string='Company')
	user_id = fields.Many2one('res.users', string="Mkt Coord")
	incoterm_id = fields.Many2one('incoterm.trade', string='Incoterms')
	payment_term_id = fields.Many2one('account.payment.term', string="Payment Terms")
	carrier_id = fields.Many2one('delivery.carrier', string='MoS')	
	financial_year = fields.Many2one('fin.year', string='Financial Year')
	currency_id = fields.Many2one('res.currency', string='Currency')
	amount = fields.Monetary("PI Amount")
	#SHIPPING LINE CHARGES
	procurement_panel_line = fields.One2many('procurement.panel.line', 'procurement_id', string="Procurement Line") 
	state = fields.Selection([('draft','Draft'),('approve','Approve'),('reject','Reject')], string="State", default="draft")
	active = fields.Boolean(
        'Active', default=True,
        help="If unchecked, it will allow you to hide the PO without removing it.")

	
	@api.multi
	def update_proc_panel(self):
		vals = []
		proc_val = []
		purchase_order = self.env['purchase.order'].search([('origin', 'like', self.name),('state','!=','draft')])
		for purchase in purchase_order:
			procurement_panel_line = self.env['procurement.panel.line'].search([('purchase_id','=',purchase.id)])
			if not procurement_panel_line:
				vals = {'procurement_panel_line':  [(0,0, {
					'partner_id': purchase.partner_id.id,
					'currency_id': purchase.currency_id.id, 
					'currency_name': purchase.currency_id.name, 
					'purchase_id': purchase.id or '', 									
					'purchase_date': purchase.date_order, 
					'coordinator_id': purchase.proc_name and purchase.proc_name.id or '', 
					'order_reference': purchase.other_ref, 
					'untaxed_amount': purchase.amount_untaxed,
					'tax_amount': purchase.amount_tax, 
					#'freight': purchase.freight, 			
					'amount_total':purchase.amount_total, 
					'amount_total1':purchase.amount_total, 
					'amount_total_inr': purchase.amount_total * 1,
					'remarks': purchase.Addi_info, 
				})],}	
				self.write(vals)
			if procurement_panel_line:
				procurement_panel_line.update({
					'partner_id': purchase.partner_id.id, 
					'currency_id': purchase.currency_id.id, 
					'currency_name': purchase.currency_id.name, 
					'purchase_id': purchase.id or '', 									
					'purchase_date': purchase.date_order, 
					'coordinator_id': purchase.proc_name and purchase.proc_name.id or '', 
					'order_reference': purchase.other_ref, 
					'untaxed_amount': purchase.amount_untaxed,
					'tax_amount': purchase.amount_tax, 
					#'freight': purchase.freight, 			
					'amount_total':purchase.amount_total, 
					'amount_total1':purchase.amount_total,
					'amount_total_inr': purchase.amount_total * 1,
					'remarks': purchase.Addi_info, 
				})

	
	
	@api.multi
	def update_procurement_panel(self):
		vals = []
		proc_val = []
		sale_order = self.env['sale.order'].search([('state','not in',('draft','cancel','sent'))])
		for order in sale_order:
			procurement_panel = self.env['procurement.panel'].search([('order_id','=',order.id)])
			if not procurement_panel:
				print"-----------if-order-----------",order,self.env.user
				proc_val = {
						'name': order.name, 
						'order_id': order.id, 
						'order_date': order.date_order,
						'partner_id': order.partner_id.id, 
						'country_id': order.partner_id.country_id.id,
						'currency_id': order.partner_id.property_product_pricelist.currency_id.id,
						'company_id': order.company_id.id,	
						'user_id': order.user_id.id, 								
						'carrier_id': order.carrier_id and order.carrier_id.id,
						'incoterm_id': order.incoterms.id, 
						'payment_term_id': order.payment_term_id.id,						
						'financial_year':order.target_year and order.target_year.id, 
						'amount': order.full_total,
					}	
				procurement_panel_id = self.env['procurement.panel'].create(proc_val)
			if procurement_panel:
				print"-----------else-order-----------",order,order.partner_id,order.partner_id.property_product_pricelist
				purchase_order = self.env['purchase.order'].search([('origin', 'like', order.name),('state','!=','draft')])
				for purchase in purchase_order:
					procurement_panel_line = self.env['procurement.panel.line'].search([('purchase_id','=',purchase.id)])
					if not procurement_panel_line:
						vals = {'procurement_panel_line':  [(0,0, {
							'partner_id': purchase.partner_id.id,
							'currency_id': purchase.currency_id.id, 
							'currency_name': purchase.currency_id.name, 
							'purchase_id': purchase.id or '', 									
							'purchase_date': purchase.date_order, 
							'coordinator_id': purchase.proc_name and purchase.proc_name.id or '', 
							'order_reference': purchase.other_ref, 
							'untaxed_amount': purchase.amount_untaxed,
							'tax_amount': purchase.amount_tax, 
							#'freight': purchase.freight, 			
							'amount_total':purchase.amount_total, 
							'amount_total1':purchase.amount_total, 
							'amount_total_inr': purchase.amount_total * 1,
							'remarks': purchase.Addi_info, 
						})],}	
						procurement_panel.write(vals)

					if procurement_panel_line:
						#for line in procurement.procurement_panel_line:
						#	line.unlink()
						procurement_panel_line.update({
							'partner_id': purchase.partner_id.id, 
							'currency_id': purchase.currency_id.id, 
							'currency_name': purchase.currency_id.name, 
							'purchase_id': purchase.id or '', 									
							'purchase_date': purchase.date_order, 
							'coordinator_id': purchase.proc_name and purchase.proc_name.id or '', 
							'order_reference': purchase.other_ref, 
							'untaxed_amount': purchase.amount_untaxed,
							'tax_amount': purchase.amount_tax, 
							#'freight': purchase.freight, 			
							'amount_total':purchase.amount_total, 
							'amount_total1':purchase.amount_total,
							'amount_total_inr': purchase.amount_total * 1,
							'remarks': purchase.Addi_info, 
						})	

	@api.multi
	def approve_order(self):
		print"-----self---appr----",self.env.user
		self.state = 'approve'
		executed_id = self.env['old.export'].search([('order_no','=',self.name)])
		for executed_sale in executed_id:
			executed_sale.total_purchase = sum(line.amount_total_inr for line in self.procurement_panel_line) - sum(line.tax_amount for line in self.procurement_panel_line)

	@api.multi
	def reject_order(self):
		print"-----self---reject----",self.env.user
		self.state = 'reject'

	@api.multi
	def unlink_procurement_panel(self):
		for procurement in self.search([]):
			for line in procurement.procurement_panel_line:
				if not line.purchase_id:
					line.unlink()
				if line.purchase_id:
					if not line.procurement_id.order_id.name in line.purchase_id.origin:
						line.unlink()


class ProcurementPanelLine(models.Model):
	_name = "procurement.panel.line"

	"""
	@api.depends('conversion_rate')
	def compute_inr(self):
		for rec in self:
			print"------- compute_inr ----",rec
			if rec.conversion_rate > 0:
				rec.amount_total_inr = rec.amount_total * rec.conversion_rate
	"""
	@api.depends('freight','packing_cost','conversion_rate')
	def compute_amount_all(self):
		for rec in self:
			print"-------compute_amount_all ----",rec
			amount_total = rec.amount_total1 + rec.freight + rec.packing_cost
			rec.amount_total = amount_total
			rec.amount_total_inr = amount_total * rec.conversion_rate

	procurement_id = fields.Many2one('procurement.panel', string="procurement ID")
	partner_id = fields.Many2one('res.partner', string='Supplier')
	purchase_id = fields.Many2one('purchase.order', string='PO No.')
	purchase_date = fields.Date('PO Date')
	coordinator_id = fields.Many2one('hr.employee', string='PO Coord.')
	order_reference = fields.Char('Order Ref')
	currency_id = fields.Many2one('res.currency', string='Currency')
	currency_name = fields.Char('Currency Name')
	untaxed_amount = fields.Monetary('Untaxed Amt')
	tax_amount = fields.Monetary('Tax Amt')
	freight = fields.Monetary('Freight')
	packing_cost = fields.Monetary('Pack. Cost')
	amount_total = fields.Monetary(compute="compute_amount_all", string='Amt Total')
	conversion_rate = fields.Float(string="Conversion Rate", default=1.0)
	amount_total1 = fields.Monetary('Amount Total1')
	amount_total_inr = fields.Monetary(compute='compute_amount_all', string='Amt Total(INR)', store=True)
	remarks = fields.Text("Remarks")
