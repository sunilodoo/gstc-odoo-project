# -*- coding: utf-8 -*-
from odoo import models, fields, osv, api, _
from odoo.tools.translate import _
from odoo.exceptions import Warning
from datetime import timedelta
import datetime

class POItemHistory2(models.Model):
	_name = 'po_item.history2'
	_order = "so_priority,priority asc"
	
	name = fields.Char('Item Description')
	product_id = fields.Many2one('product.product', string='Item')
	product_uom_qty = fields.Float(string='Qty.', required=True, default=1.0)
	product_uom = fields.Many2one('product.uom', string='Unit', required=True)
	unit_price = fields.Float(string='Rate')
	price_subtotal = fields.Float(compute='_compute_amount', string='Amount', readonly=True, store=True)
	pf_chrg = fields.Float('P&F Charges')
	vendor = fields.Many2one('res.partner', string='Vendor', domain = "[('supplier','=',True)]")
	buyer = fields.Many2one('res.partner', string='Buyer')
	proc_name = fields.Many2one('hr.employee', string='Procu. Coordinator')
	so_id = fields.Many2one('sale.order', string='SO No.', readonly=True)
	po_id = fields.Many2one('purchase.order', string='PO No.', readonly=True)
	priority = fields.Char('PO Priority')
	so_priority = fields.Char('SO Priority')
	po_place_date = fields.Date('PO Placed date', readonly=True)
	dlvy_confm_date = fields.Date('DLVY Confirm date', readonly=True)
	dlvy_req_date = fields.Date('DLVY req. Date', readonly=True)
	oe_dlvy_req_date = fields.Date('Original EXP DLVY date', readonly=True)
	cur_dlvy_date = fields.Date('Current DLVY date', readonly=True)
	act_dlvy_date = fields.Date('Actual DLVY date', readonly=True)
	inv_date = fields.Date('Invoice date', readonly=True)
	bill_no = fields.Char('Bill No')
	bill_date = fields.Date('Bill date', readonly=True)
	sob_date = fields.Date('SOB date', readonly=True)
	doc_bank_date = fields.Date('Docs to bank date', readonly=True)
	remarks = fields.Text('Remarks')
	is_problem = fields.Boolean('?', default=False)
	problem = fields.Text('Problems')
	pack_docs_day = fields.Date('Packing & docs days', readonly=True)
	days_dispatch = fields.Integer('Days to Dispatch', readonly=True)
	state = fields.Char('Status')
	status = fields.Selection([('draft', 'Draft'),('cancel', 'Cancel'),('open', 'Open'),('done', 'Closed')],string='Status', track_visibility='onchange', default='draft')

	os_qty = fields.Float('OS PO Qty.')
	goods_rcvd_qty = fields.Float('Goods Rcvd Qty.')
	goods_insp_qty = fields.Float('Goods Insp Qty')
	goods_packed = fields.Float('Packed Qty.')
	avl_qty = fields.Float('Available Stock')
	
	@api.multi
	@api.onchange('product_id')
	def change_product(self):
		print"--------------======-------",self.product_id
		vals = {}
		if self.product_id:
			vals['name'] = self.product_id.name
			vals['product_uom'] = self.product_id.uom_id
			vals['unit_price'] = self.product_id.lst_price
		self.update(vals)

	@api.depends('product_uom_qty', 'unit_price')
	def _compute_amount(self):
		print"---------------=====-------",self.product_uom_qty
		for rec in self:
			rec.price_subtotal = rec.product_uom_qty * rec.unit_price

	@api.multi
	def write(self, values):
		print"----))))))))))))))))))----------------",values
		values['price_subtotal'] = self.product_uom_qty * self.unit_price
		result = super(POItemHistory2, self).write(values)
		return result

	@api.onchange('oe_dlvy_req_date')
	def change_date(self):
		print"--------------======-------",self.oe_dlvy_req_date
		if self.oe_dlvy_req_date :
			self.pack_docs_day = datetime.datetime.strptime(self.oe_dlvy_req_date, '%Y-%m-%d') + datetime.timedelta(days=5)
		if self.po_place_date and self.oe_dlvy_req_date :
			diff = datetime.datetime.strptime(self.pack_docs_day, '%Y-%m-%d') - datetime.datetime.strptime(self.po_place_date, '%Y-%m-%d')
			self.days_dispatch = diff.days
	
'''
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

