# -*- coding: utf-8 -*-
from odoo import models, fields, osv, api, _
from odoo.tools.translate import _
from odoo.exceptions import Warning
from datetime import timedelta
import datetime

class POMisReporting(models.Model):
	_name = 'po_mis.reporting'
	
	name = fields.Many2one('hr.employee', string='Mkt. Coordinator')
	po_coord = fields.Many2one('hr.employee', string='PO Coordinator')
	po_no = fields.Char('PO Number')
	po_date = fields.Date('PO Date')
	buyer = fields.Many2one('res.partner', string='Buyer')
	country = fields.Many2one('res.country', 'Country')
	destination = fields.Char('Final Destination port')
	amount = fields.Float('Amount')
	mode = fields.Many2one('delivery.carrier', string='Mode of Shipment')
	incoterm = fields.Many2one('stock.incoterms', string='Incoterms')
	payment_term = fields.Many2one('account.payment.term', string='Payment Terms')
	payment_status = fields.Many2one('payment.status', string='Payment Status')
	recvd_amount = fields.Float('Received Amount')
	edrg = fields.Date('Expect Date of Receiving Goods')
	etd = fields.Date('Expect Date Dispatch')
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



