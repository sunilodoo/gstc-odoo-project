# -*- coding: utf-8 -*-
from odoo import models, fields, osv, api, _
from odoo.tools.translate import _
from odoo.exceptions import Warning
from datetime import timedelta
import datetime

class POMisReporting(models.Model):
	_inherit = 'mail.thread'
	_name = 'po_mis.reporting'
	
	name = fields.Many2one('hr.employee', string='Mkt. Coordinator')
	po_coord = fields.Many2one('hr.employee', string='SO Coordinator')
	po_no = fields.Many2one('sale.order', string='SO No.')
	po_date = fields.Date('SO Date')
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
	oedd = fields.Date('Original EDD')
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

	@api.onchange('po_coord')
	def change_po_coord(self):
		print"-------------po_coord-======-------",self.po_coord
		mis = self.env['mis.reporting'].search([('order_id.name','=',self.po_no.name)])
		if self.po_coord and mis:
			mis.write({'proc_name': self.po_coord.id})

	@api.onchange('edrg')
	def change_date(self):
		print"--------------======-------",self.edrg
		#if not self.edrg :
		#	raise Warning(_("Buyer's country not defined! "))
		mis = self.env['mis.reporting'].search([('order_id.name','=',self.po_no.name)])
		if self.edrg :
			self.etd = datetime.datetime.strptime(self.edrg, '%Y-%m-%d') + datetime.timedelta(days=7)
			if mis:
				mis.write({'edd': self.etd})

	@api.multi
	def po_detalis(self):
		#po = self.env['purchase.order'].search([('origin', 'like', self.order_id.name)])
		l = []
		
		po = self.env['purchase.order'].search([('origin', 'like', self.po_no.name)])
		if not po:
			raise Warning(_("SO not Found! "))
		for p in po:
			#if not p.state in ['draft','sent']:
			p_mis = self.env['po_item.history2'].search([('po_id', '=', p.id)])
			for pm in p_mis:
				l.append(pm.id)
		ids = [m for m in l]
		return {
			'name':   ('Summary PO'),
			'view_type': 'form',
			'view_mode': 'tree,form',
			'res_model': 'po_item.history2',
			'context':self._context,
			'domain':[('id','in',ids)],
			'type': 'ir.actions.act_window',
			'target': 'current',
			'flags': {'form': {'action_buttons': True}}
		}	

class PaymentStatus(models.Model):
	_name = 'payment.status'
	
	name = fields.Char(string='Name')



