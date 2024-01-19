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
	origin = fields.Char('Source Document', copy=True)
	company_id = fields.Many2one('res.company', string='Company', copy=True)
	partner_id = fields.Many2one("res.partner", string="Customer", copy=True)	
	is_consignee = fields.Boolean('Inv to consignee', copy=True)
	consignee = fields.Many2one('res.partner', string='Consignee', copy=True)
	payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms', copy=True)
	date_invoice = fields.Date('Invoice Date', copy=True)
	user_id = fields.Many2one('res.users', string='Salesperson', copy=True)
	team_id = fields.Many2one('crm.team', string='Sales Team', copy=True)
	currency_id = fields.Many2one('res.currency', string='Currency', copy=True)
	packing_line_ids = fields.One2many('packing.line', 'pack_id', string='Packing Lines', copy=True)
	#hide_dispatch=fields.Boolean('Hide',default=False)
	inv_no = fields.Char('Invoice No.', copy=True)
	order_no = fields.Char("Buyer's Order No", copy=True)
	order_date = fields.Date("Buyer's Order Date", copy=True)
	origin_country = fields.Char('Country of Origin', required=True, copy=True)
	dest_country = fields.Char('Country of Destination', required=True, copy=True)
	pre_carrier = fields.Char('Pre-carrier By', copy=True)
	flight_no = fields.Char('Vessel/Flight No', copy=True)
	port_discharge = fields.Char('Port of Discharge', required=True, copy=True)
	pl_receipt = fields.Char('Place of Receipt', copy=True)
	port_loading = fields.Char('Port of Loading', copy=True)
	final_dest = fields.Char('Final Destination', required=True, copy=True)
	container_no = fields.Char('Marks & No.s/Container No', copy=True)
	container_no1 = fields.Char('Marks & No.s/Container1 No', copy=True)
	container_no2 = fields.Char('Marks & No.s/Container2 No', copy=True)
	kind_pkg = fields.Char('No. & Kind of Pkgs.', copy=True)
	kind_pkg_unit = fields.Many2one('product.uom', string='Pkgs. Unit', copy=True)
	commodity_desc = fields.Text('Commodity & Other Description', copy=True)
	iec_no = fields.Char('IEC No.', copy=True)
	total_grwt = fields.Float(string='Total Gross Weight', store=True, compute='_calculate_weight', track_visibility='always')
	total_ntwt = fields.Float(string='Total Net Weight', store=True, compute='_calculate_weight', track_visibility='always')
	total_carton = fields.Float(string='Total Carton', store=True, compute='_calculate_weight', track_visibility='always')
	total_vol = fields.Float(string='Volume(approx)', store=True, compute='_calculate_volume', track_visibility='always')
	total_vol_manuall = fields.Float(string='Total Volume', track_visibility='always')
	inv_id = fields.Many2one('account.invoice', string='Inv', copy=True)
	vol_unit = fields.Many2one('product.uom', string='Unit', copy=True)
	carrier_id = fields.Many2one('delivery.carrier', string="Mode of Shipment")
	incoterms = fields.Many2one('incoterm.trade','Incoterm')
	target_year = fields.Many2one('fin.year', string='Financial Year', track_visibility='always', related='inv_id.target_year', store=True)

	@api.model
	def create(self, vals):
		seq = self.env['ir.sequence'].next_by_code('packing.list') or '/'
		vals['name'] = seq
		return super(PackingList, self).create(vals)

	@api.multi
	@api.depends('packing_line_ids.gross_wt','packing_line_ids.net_wt',)
	def _calculate_weight(self):
		total_gw = total_nw = total_carton = l = b = h = 0.0
		for packing in self:
			invoice = self.env['account.invoice'].search([('id','=',packing.inv_id.id)])
			for line in packing.packing_line_ids:
				total_gw += line.gross_wt * float(line.crtns)
				total_nw += line.net_wt * float(line.crtns)
				total_carton += float(line.crtns)
			packing.total_grwt = total_gw
			packing.total_ntwt = total_nw
			packing.total_carton = total_carton
			packing.kind_pkg = int(total_carton)

	@api.multi
	@api.depends('packing_line_ids.measurement','packing_line_ids.crtns')
	def _calculate_volume(self):
		volume = total_vol = l = b = h = 0.0
		for packing in self:
			for line in packing.packing_line_ids:
				if line.measurement: 
					if 'x' in line.measurement:
						l = line.measurement.split('x')[0] or ''
						b = line.measurement.split('x')[1] or ''
						h = line.measurement.split('x')[2] or ''
					elif 'X' in line.measurement:
						l = line.measurement.split('X')[0] or ''
						b = line.measurement.split('X')[1] or ''
						h = line.measurement.split('X')[2] or ''
					else:
						pass
					carton = line.crtns
					volume += (float(l)*float(b)*float(h)*float(line.crtns))
			print"--------====volume=====----l--b--h-----",volume,l,b,h
			if packing and (packing.order_no or packing.origin):
				#order = self.env['sale.order'].search([('name','=',packing.origin)])
				#print"--------order-----packing------",order
				#if order and order.carrier_id:
				if packing.carrier_id.name == 'By Air' or packing.carrier_id.name == 'By AIR':
					packing.total_vol = volume/6000
				if packing.carrier_id.name == 'By APP':
					packing.total_vol = volume/6000
				if packing.carrier_id.name == 'By Sea' or packing.carrier_id.name == 'By SEA':
					packing.total_vol = volume/1000000
				if packing.carrier_id.name == 'By SPP':
					packing.total_vol = volume/1000000
				if packing.carrier_id.name == 'By Courier':
					packing.total_vol = volume/5000
				print"---------packing.total_vol------",packing.total_vol

	@api.onchange('carrier_id')
	def onchange_carrier_id(self):
		self._calculate_volume()
	@api.onchange('pre_carrier','flight_no','port_discharge','final_dest','container_no','container_no1',
'container_no2','kind_pkg','kind_pkg_unit','commodity_desc')
	def change_commodity(self):
		for pl in self:
			invoice_id = self.env['account.invoice'].search([('id','=',pl.inv_id.id)])
			for invoice in invoice_id:
				invoice.write({'pre_carrier': pl.pre_carrier, 'flight_no': pl.flight_no, 'port_discharge': pl.port_discharge, 'final_dest': pl.final_dest, 'container_no': pl.container_no, 'container_no1': pl.container_no1, 'container_no2':pl.container_no2, 'kind_pkg': pl.kind_pkg, 'kind_pkg_unit':pl.kind_pkg_unit and pl.kind_pkg_unit.id, 'commodity_desc': pl.commodity_desc})

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
	carton_no = fields.Char('Package No.')
	gross_wt = fields.Float('Gross Weight')
	net_wt = fields.Float('Net Weight')
	measurement = fields.Char(string='Measurement', help="It must be like axbxc!")
	crtns = fields.Char('Cartons')
	product_id = fields.Many2one('product.product', string='Product')
	name = fields.Char('Description', required=True)
	order_qty = fields.Float('Order Qty')
	quantity = fields.Float('Quantity')
	uom_id = fields.Many2one('product.uom', string='Unit of Measure')
	remarks = fields.Char('Remarks')
#	price_unit = fields.Float('Unit Price')
#	tax_id = fields.Many2many('account.tax', string='Tax')
#	price_subtotal = fields.Float('Amount')

	@api.onchange('quantity')
	def change_quantity(self):
		print"-------change_quantity----self-------",self,self._origin.id,self.pack_id.inv_id,self.product_id.id
		invoice_line_ids = self.env['account.invoice.line'].search([('invoice_id','=', self.pack_id.inv_id.id),('product_id','=',self.product_id.id)])
		for line in invoice_line_ids:
			total_p_qty = 0
			if line:
				packing_l = self.env['packing.line'].search([('product_id', '=', self.product_id.id),('pack_id.inv_id','=', line.invoice_id.id),('quantity','!=',self.quantity)])

				for p_qty in packing_l:
					total_p_qty = p_qty.quantity + self.quantity
				#total_p_qty = sum(l.quantity for l in packing_l)
				print"---------==product_id.id==",line.product_id.id,packing_l,self.product_id.id,total_p_qty,self.quantity
				line.write({'quantity': total_p_qty})

		export_line_ids = self.env['export.line'].search([('export_id.inv_id','=', self.pack_id.inv_id.id),('product_id','=',self.product_id.id)])
		if export_line_ids:
			print"---------invoice_line_ids=====",invoice_line_ids
			export_line_ids.write({'quantity': self.quantity})


	@api.multi
	def line_copy(self):
		data = self.copy_data()
		sale_order_obj = self.env['packing.list']
		print"-----------dac--copy---line",data,self.pack_id
		if data:
			li = self.create(data[0])
			print"--------li----------",li
		else:
			raise UserError(_("Can't Copy this line"))			




