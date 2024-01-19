# -*- coding: utf-8 -*-
from odoo import models, fields, osv, api, _
from odoo.tools.translate import _
from odoo.exceptions import Warning
from datetime import timedelta
import datetime

class POItemHistory(models.Model):
	_name = 'po_item.history'
	
	name = fields.Many2one('product.product', string='Item')
	descr = fields.Char('Item Description')
	product_uom_qty = fields.Float(string='Qty.', required=True, default=1.0)
	product_uom = fields.Many2one('product.uom', string='Unit', required=True)
	unit_price = fields.Float(string='Rate')
	price_subtotal = fields.Float(compute='_compute_amount', string='Amount', readonly=True, store=True)
	pf_chrg = fields.Float('P&F Charges')
	buyer = fields.Many2one('res.partner', string='Buyer')
	po_place_date = fields.Date('PO Placed date')
	dlvy_confm_date = fields.Date('DLVY Confirm date')
	dlvy_req_date = fields.Date('DLVY req. Date')
	oe_dlvy_req_date = fields.Date('Original EXP DLVY date')
	cur_dlvy_date = fields.Date('Current DLVY date')
	act_dlvy_date = fields.Date('Actual DLVY date')
	inv_date = fields.Date('Invoice date')
	bill_no = fields.Char('Bill No')
	bill_date = fields.Date('Bill date')
	sob_date = fields.Date('SOB date')
	doc_bank_date = fields.Date('Docs to bank date')
	remarks = fields.Text('Remarks')
	is_problem = fields.Boolean('Is Problem?', default=False)
	problem = fields.Text('Problems')
'''
	po_coord = fields.Many2one('hr.employee', string='PO Coordinator')

	po_date = fields.Date('PO Date')
	
	country = fields.Many2one('res.country', 'Country')
	destination = fields.Char('Final Destination port')
	amount = fields.Float('Amount')
	mode = fields.Many2one('delivery.carrier', string='Mode of Shipment')
	incoterm = fields.Many2one('stock.incoterms', string='Incoterms')
	payment_term = fields.Many2one('account.payment.term', string='Payment Terms')
	payment_status = fields.Many2one('payment.status', string='Payment Status')
	recvd_amount = fields.Float('Received Amount')
	
	remarks = fields.Text('Remarks')
	dispatch_month = fields.Date('Dispatch Month')
	invoice = fields.Char('Invoice Number')
	invoice_val = fields.Float('Invoice Value')
	invoice_date = fields.Date('Invoice Date')
	balance = fields.Float('Balance amount')
	currency = fields.Many2one('res.currency', string='Currency')
	

	@api.onchange('buyer')
	def change_country(self):
		print"--------------======-------",self.buyer
		if not (self.buyer and self.buyer.country_id):
			raise Warning(_("Buyer's country not defined! "))
		if self.buyer and self.buyer.country_id:
			self.country = self.buyer.country_id.id

	@api.onchange('edrg')
	def change_date(self):
		print"--------------======-------",self.edrg
		#if not self.edrg :
		#	raise Warning(_("Buyer's country not defined! "))
		if self.edrg :
			self.etd = datetime.datetime.strptime(self.edrg, '%Y-%m-%d') + datetime.timedelta(days=7)

class PaymentStatus(models.Model):
	_name = 'payment.status'
	
	name = fields.Char(string='Name')

'''

