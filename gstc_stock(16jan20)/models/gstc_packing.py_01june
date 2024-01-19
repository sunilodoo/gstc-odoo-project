# -*- coding: utf-8 -*-

from odoo import models, fields, osv, api, _
from odoo.tools.translate import _
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import Warning, UserError
from datetime import timedelta
import datetime

class PackingList(models.Model):
	_name = "packing.list"

	name = fields.Char('Name')
	origin = fields.Char('Source Document')
	company_id = fields.Many2one('res.company', string='Company')
	partner_id = fields.Many2one("res.partner", string="Customer")	
	is_consignee = fields.Boolean('Inv to consignee')
	consignee = fields.Many2one('res.partner', string='Consignee')
	payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms')
	date_invoice = fields.Date('Invoice Date')
	user_id = fields.Many2one('res.users', string='Salesperson')
	team_id = fields.Many2one('crm.team', string='Sales Team')
	currency_id = fields.Many2one('res.currency', string='Currency')
	packing_line_ids = fields.One2many('packing.line', 'pack_id', string='Packing Lines')
	#hide_dispatch=fields.Boolean('Hide',default=False)
	inv_no = fields.Char('Invoice No.')
	order_no = fields.Char("Buyer's Order No")
	order_date = fields.Date("Buyer's Order Date")
	origin_country = fields.Char('Country of Origin')
	dest_country = fields.Char('Country of Destination')
	pre_carrier = fields.Char('Pre-carrier By')
	flight_no = fields.Char('Vessel/Flight No')
	port_discharge = fields.Char('Port of Discharge')
	pl_receipt = fields.Char('Place of Receipt')
	port_loading = fields.Char('Port of Loading')
	final_dest = fields.Char('Final Destination')
	container_no = fields.Char('Marks & No.s/Container No')
	container_no1 = fields.Char('Marks & No.s/Container1 No')
	container_no2 = fields.Char('Marks & No.s/Container2 No')
	kind_pkg = fields.Char('No. & Kind of Pkgs.')
	commodity_desc = fields.Text('Commodity & Other Description')
	iec_no = fields.Char('IEC No.')
	total_grwt = fields.Float('Total Gross Weight')
	total_ntwt = fields.Float('Total Net Weight')
	total_vol = fields.Float('Total Volume')
	inv_id = fields.Many2one('account.invoice', string='Inv')

	@api.model
	def create(self, vals):
		seq = self.env['ir.sequence'].next_by_code('packing.list') or '/'
		vals['name'] = seq
		return super(PackingList, self).create(vals)

	'''
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
	'''
	
class PackingLine(models.Model):
	_name = "packing.line"

	pack_id = fields.Many2one("packing.list", string="Pack ID")	
	carton_no = fields.Char('Carton No.')
	gross_wt = fields.Float('Gross Weight')
	net_wt = fields.Float('Net Weight')
	measurement = fields.Char('Measurement')
	#product_id = fields.Many2one('product.product', string='Product')
	name = fields.Char('Description', required=True)
	quantity = fields.Float('Quantity')
	uom_id = fields.Many2one('product.uom', string='Unit of Measure')
	remarks = fields.Char('Remarks')
#	price_unit = fields.Float('Unit Price')
#	tax_id = fields.Many2many('account.tax', string='Tax')
#	price_subtotal = fields.Float('Amount')




