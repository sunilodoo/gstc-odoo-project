# -*- coding: utf-8 -*-

from odoo import models, fields, osv, api, _
from odoo.tools.translate import _
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import Warning, UserError
from datetime import timedelta
import datetime

class AccountInvoice(models.Model):
	_inherit = "account.invoice"

	@api.one
	@api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'currency_id', 'company_id', 'date_invoice', 'type')
	def _compute_amount(self):
		result = super(AccountInvoice,self)._compute_amount()
		self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line_ids)
		self.amount_tax = sum(line.amount for line in self.tax_line_ids)
		print"------------------result-----------",result
		self.amount_total = self.amount_untaxed + self.amount_tax + self.freight_charge + self.bank_charge + self.ext_charge - self.global_disc
		#result.update({'amount_total':
		return result

	is_consignee = fields.Boolean('Inv to consignee')
	consignee = fields.Many2one('res.partner', string='Consignee')
	hide_dispatch=fields.Boolean('Hide',default=False)
	packing_flag=fields.Boolean('Packing Flag',default=False)
	export_flag=fields.Boolean('Export Flag',default=False)
	inv_no = fields.Char('Invoice No.')
	order_no = fields.Char("Buyer's Order No")
	order_date = fields.Date("Buyer's Order Date")
	origin_country = fields.Char('Country of Origin')
	dest_country = fields.Many2one('res.country', string='Country of Destination')
	pre_carrier = fields.Char('Pre-carrier By')
	flight_no = fields.Char('Vessel/Flight No')
	port_discharge = fields.Char('Port of Discharge')
	pl_receipt = fields.Char('Place of Receipt')
	port_loading = fields.Char('Port of Loading')
	final_dest = fields.Char(string='Final Destination')
	container_no = fields.Char('Marks & No.s/Container No')
	container_no1 = fields.Char('Marks & No.s/Container1 No')
	container_no2 = fields.Char('Marks & No.s/Container2 No')
	kind_pkg = fields.Char('No. & Kind of Pkgs.')
	commodity_desc = fields.Text('Commodity & Other Description')
	iec_no = fields.Char('IEC No.')
	total_grwt = fields.Float('Total Gross Weight')
	total_ntwt = fields.Float('Total Net Weight')
	packing_count = fields.Integer(compute='_compute_packing', string='Packing', default=0)
	freight_charge = fields.Monetary('Freight & Insurance')
	global_disc = fields.Monetary('Discount')
	bank_charge = fields.Monetary('Banking & Handling')
	ext_charge = fields.Monetary('Extra Charges')
	#grand_total = fields.Monetary('Grand Total')
	export_count = fields.Integer(compute='_compute_export', string='Export', default=0)


	@api.multi
	@api.model
	def dispatch(self):
		dis=True
		origin=self.origin
		if origin and ('SO' in origin):
			order=self.env['sale.order'].search([('name','=like',origin)],limit=1)
			purchase_orders=self.env['purchase.order'].search([('origin','like',origin)])
			for po in purchase_orders:
				if po.picking_ids:
					for pick in po.picking_ids:
						if (pick.state != 'done'): 
							dis=False
							break
					if not dis:
						break
				else:
					raise UserError(_("Purchase Order Not Confirmed"))
		
			if dis:
				if order:
					for picks in order.picking_ids:
						if picks.state not in ['draft','cancel','done']:
							picks.force_assign()
							wiz = self.env['stock.immediate.transfer'].create({'pick_id': picks.id})
							wiz.process()
							self.hide_dispatch=True
						else:
							raise UserError(_("Stock already Dispatched"))
			else:
				raise UserError(_("Shipment not Received yet!!!"))
		return
	
	@api.multi
	@api.model
	def generate_packing(self):
		print"------------context-------",self
		vals = []
		li = []
		vals = {
			'name': '',
			'origin': self.origin,
			'company_id': self.company_id.id,
			'partner_id': self.partner_id.id,
			'is_consignee': self.is_consignee,
			'consignee': self.consignee.id,
			'payment_term_id': self.payment_term_id.id,
			'date_invoice': self.date_invoice,
			'user_id': self.user_id.id,
			'team_id': self.team_id.id,
			'currency_id': self.currency_id.id,
			'inv_no': self.inv_no,
			'order_no': self.order_no,
			'order_date': self.order_date,
			'origin_country': self.origin_country,
			'dest_country': self.dest_country and self.dest_country.name or '',
			'pre_carrier': self.pre_carrier,
			'flight_no': self.flight_no,
			'port_discharge': self.port_discharge,
			'pl_receipt': self.pl_receipt,
			'port_loading': self.port_loading,
			'final_dest': self.final_dest,
			'container_no': self.container_no,
			'container_no1': self.container_no1,
			'container_no2': self.container_no2,
			'kind_pkg': self.kind_pkg,
			'commodity_desc': self.commodity_desc,
			'iec_no': self.iec_no,
			'total_grwt': self.total_grwt,
			'total_ntwt': self.total_ntwt,
			#'total_vol': self.total_vol,
			'inv_id': self.id,
		}
		pack = self.env['packing.list'].create(vals)
		for line in self.invoice_line_ids:
			li = {'packing_line_ids':  [(0,0, {
				#'product_id': line.product_id.id,
				'name': line.name,
				'quantity': line.quantity,
				'uom_id': line.uom_id.id,
			})],}
			pack.write(li)
		self.packing_flag = True
		print"-------------pack-------",pack

	@api.multi
	@api.model
	def generate_export(self):
		print"------------context-------",self
		vals = []
		li = []
		vals = {
			'name': '',
			'origin': self.origin,
			'company_id': self.company_id.id,
			'partner_id': self.partner_id.id,
			'is_consignee': self.is_consignee,
			'consignee': self.consignee.id,
			'payment_term_id': self.payment_term_id.id,
			'date_invoice': self.date_invoice,
			'currency_id': self.currency_id.id,
			'inv_no': self.inv_no,
			'transport_mode': self.pre_carrier,
			'supply_place': self.pl_receipt,
			'total_grwt': self.total_grwt,
			#'total_cartons': self.total_ntwt,
			'freight_charge': self.freight_charge,
			'bank_charge': self.bank_charge,
			'ext_charge': self.ext_charge,
			'global_disc': self.global_disc,
			'grand_total': self.amount_total,
			'inv_id': self.id,
		}
		export = self.env['export.invoice'].create(vals)
		for line in self.invoice_line_ids:
			li = {'export_line_ids':  [(0,0, {
				#'product_id': line.product_id.id,
				'name': line.name,
				'quantity': line.quantity,
				'uom_id': line.uom_id.id,
				'price_unit1': line.price_unit,
				'price_unit': line.price_unit,
				'discount': self.global_disc / len(self.invoice_line_ids),
				'price_subtotal': line.quantity  * line.price_unit,
			})],}
			export.write(li)
		self.export_flag = True
		print"-------------export.invoice-------",export

	@api.multi
	@api.model
	def action_view_packing(self):

		l = []
		packings = self.env['packing.list'].search([('inv_id','=',self.id)])
		print"================packing=========wiz==",packings
		if not packings:
			raise Warning(_("Packing List Not Found! "))
		for p in packings:
			l.append(p.id)
		ids = [m for m in l]
		return {
			'name':   ('Packing List'),
			'view_type': 'form',
			'view_mode': 'tree,form',
			'res_model': 'packing.list',
			'context':self._context,
			'domain':[('id','in',ids)],
			'type': 'ir.actions.act_window',
			'target': 'current',
			'flags': {'form': {'action_buttons': True}}
		}

	@api.multi
	@api.model
	def action_view_export(self):

		l = []
		export = self.env['export.invoice'].search([('inv_id','=',self.id)])
		print"================packing=========wiz==",export
		if not export:
			raise Warning(_("Export Invoice Not Found! "))
		for p in export:
			l.append(p.id)
		ids = [m for m in l]
		return {
			'name':   ('Export Invoice'),
			'view_type': 'form',
			'view_mode': 'tree,form',
			'res_model': 'export.invoice',
			'context':self._context,
			'domain':[('id','in',ids)],
			'type': 'ir.actions.act_window',
			'target': 'current',
			'flags': {'form': {'action_buttons': True}}
		}

	@api.depends('invoice_line_ids')
	def _compute_packing(self):
		for order in self:
			packings = self.env['packing.list'].search([('inv_id','=',self.id)])
			order.packing_count = len(packings)

	@api.depends('invoice_line_ids')
	def _compute_export(self):
		for order in self:
			export = self.env['export.invoice'].search([('inv_id','=',self.id)])
			order.export_count = len(export)






