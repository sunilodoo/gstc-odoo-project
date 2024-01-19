# -*- coding: utf-8 -*-

from odoo import models, fields, osv, api, _
from odoo.tools.translate import _
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import Warning, UserError
from datetime import timedelta
import datetime
import logging

_logger = logging.getLogger(__name__)

class AccountInvoice(models.Model):
	_inherit = "account.invoice"

	@api.one
	@api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'currency_id', 'company_id', 'date_invoice', 'type','insurance_only','freight_charge','freight_only','global_disc','bank_charge','ext_charge')
	def _compute_amount(self):
		result = super(AccountInvoice,self)._compute_amount()
		self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line_ids)
		self.amount_tax = sum(line.amount for line in self.tax_line_ids)
		#print"------------------result-----------",result
		self.amount_total = self.amount_untaxed + self.amount_tax + self.freight_charge + self.freight_only + self.insurance_only + self.bank_charge + self.ext_charge - self.global_disc
		amount_total_company_signed = self.amount_total
		amount_untaxed_signed = self.amount_untaxed
		if self.currency_id and self.company_id and self.currency_id != self.company_id.currency_id:
			currency_id = self.currency_id.with_context(date=self.date_invoice)
			amount_total_company_signed = currency_id.compute(self.amount_total, self.company_id.currency_id)
			amount_untaxed_signed = currency_id.compute(self.amount_untaxed, self.company_id.currency_id)
		sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
		self.amount_total_company_signed = amount_total_company_signed * sign
		self.amount_total_signed = self.amount_total * sign
		self.amount_untaxed_signed = amount_untaxed_signed * sign

	@api.one
	@api.depends(
		'state', 'currency_id', 'invoice_line_ids.price_subtotal',
		'move_id.line_ids.amount_residual','insurance_only','freight_charge','freight_only','global_disc','bank_charge','ext_charge',
		'move_id.line_ids.currency_id')
	def _compute_residual(self):
		residual = 0.0
		residual_company_signed = 0.0
		sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
		for line in self.sudo().move_id.line_ids:
			if line.account_id.internal_type in ('receivable', 'payable'):
				residual_company_signed += line.amount_residual
				if line.currency_id == self.currency_id:
				    residual += line.amount_residual_currency if line.currency_id else line.amount_residual
				else:
				    from_currency = (line.currency_id and line.currency_id.with_context(date=line.date)) or line.company_id.currency_id.with_context(date=line.date)
				    residual += from_currency.compute(line.amount_residual, self.currency_id)
		self.residual_company_signed = abs(residual_company_signed) * sign + self.freight_charge + self.freight_only + self.insurance_only + self.bank_charge + self.ext_charge - self.global_disc
		self.residual_signed = abs(residual) * sign + self.freight_charge + self.freight_only + self.insurance_only + self.bank_charge + self.ext_charge - self.global_disc
		self.residual = abs(residual) + self.freight_charge + self.freight_only + self.insurance_only + self.bank_charge + self.ext_charge - self.global_disc
		digits_rounding_precision = self.currency_id.rounding
		if float_is_zero(self.residual, precision_rounding=digits_rounding_precision):
			self.reconciled = True
		else:
			self.reconciled = False

	is_consignee = fields.Boolean('Inv to consignee')
	consignee = fields.Many2one('res.partner', string='Consignee', copy=True)
	hide_dispatch=fields.Boolean('Hide',default=False)
	packing_flag=fields.Boolean('Packing Flag',default=False)
	export_flag=fields.Boolean('Export Flag',default=False)
	inv_no = fields.Char('Invoice No.', copy=True)
	order_no = fields.Char("Buyer's Order No", copy=True)
	order_date = fields.Date("Buyer's Order Date")
	origin_country = fields.Char('Country of Origin', required=False, copy=True)
	dest_country = fields.Many2one('res.country', string='Country of Destination', required=False, copy=True)
	pre_carrier = fields.Char('Pre-carrier By', copy=True)
	flight_no = fields.Char('Vessel/Flight No', copy=True)
	port_discharge = fields.Char('Port of Discharge', copy=True)
	pl_receipt = fields.Char('Place of Receipt', required=False, copy=True)
	port_loading = fields.Char('Port of Loading', copy=True)
	final_dest = fields.Char(string='Final Destination', required=False, copy=True)
	container_no = fields.Char('Marks & No.s/Container No', copy=True)
	container_no1 = fields.Char('Marks & No.s/Container1 No', copy=True)
	container_no2 = fields.Char('Marks & No.s/Container2 No', copy=True)
	kind_pkg = fields.Char('No. & Kind of Pkgs.', copy=True, related='packing_invoice_id.kind_pkg')
	kind_pkg_unit = fields.Many2one('product.uom', string='Pkgs. Unit', copy=True)
	commodity_desc = fields.Text('Commodity & Other Description', copy=True)
	iec_no = fields.Char('IEC No.', copy=True)
	total_grwt = fields.Float(string='Total Gross Weight', related='packing_invoice_id.total_grwt')
	total_ntwt = fields.Float(string='Total Net Weight', related='packing_invoice_id.total_ntwt')
	packing_count = fields.Integer(compute='_compute_packing', string='Packing', default=0)
	freight_charge = fields.Monetary('Freight & Insurance', copy=True)
	freight_only = fields.Monetary('Freight', copy=True)
	insurance_only = fields.Monetary('Insurance', copy=True)
	global_disc = fields.Monetary('Discount', copy=True)
	bank_charge = fields.Monetary('Banking & Handling', copy=True)
	ext_charge = fields.Monetary('Extra Charges')
	#grand_total = fields.Monetary('Grand Total')
	export_count = fields.Integer(compute='_compute_export', string='Export', default=0)
	packing_invoice_id = fields.Many2one('packing.list', string='Packing Invoice ID')
	export_invoice_id = fields.Many2one('export.invoice', string='Export Invoice ID')
	company_id = fields.Many2one('res.company', string='Company', change_default=True,
        required=True, readonly=False,
        default=lambda self: self.env['res.company']._company_default_get('account.invoice'))
	active = fields.Boolean(
        'Active', default=True,
        help="If unchecked, it will allow you to hide the PO without removing it.")
	dispatched_date = fields.Date('Dispatch Date')
	state = fields.Selection([
            ('draft','Draft'),
            ('proforma', 'Pro-forma'),
            ('proforma2', 'Pro-forma'),
            ('open', 'Open'),
            ('dispatch', 'Dispatch'),
            ('paid', 'Paid'),
            ('cancel', 'Cancelled'),
        ], string='Status', index=True, readonly=True, default='draft',
        track_visibility='onchange', copy=False,
        help=" * The 'Draft' status is used when a user is encoding a new and unconfirmed Invoice.\n"
             " * The 'Pro-forma' status is used when the invoice does not have an invoice number.\n"
             " * The 'Open' status is used when user creates invoice, an invoice number is generated. It stays in the open status till the user pays the invoice.\n"
             " * The 'Paid' status is set automatically when the invoice is paid. Its related journal entries may or may not be reconciled.\n"
             " * The 'Cancelled' status is used when user cancel invoice.")
	carrier_id = fields.Many2one('delivery.carrier', string="Mode of Shipment")
	incoterms = fields.Many2one('incoterm.trade','Incoterm')
	display_hsn = fields.Boolean("Display HS Code")
	target_year = fields.Many2one('fin.year', string='Financial Year', track_visibility='always', compute="_calculate_year", store=True)
	
	
	@api.depends('date_invoice')
	def _calculate_year(self):
		year = ''
		month = ''
		for rec in self:
			if rec.date_invoice:
				year = datetime.datetime.strptime(rec.date_invoice, '%Y-%m-%d').strftime('%Y')
				month = datetime.datetime.strptime(rec.date_invoice, '%Y-%m-%d').month
				if month <= 3:
					target_year = self.env['fin.year'].search([('name','like', '-'+str(year[2:]))])
				if month > 3:
					target_year = self.env['fin.year'].search([('name','ilike', year)], limit=1)
					for ty in target_year :
						rec.target_year = ty.id
			else:
				rec.target_year = ''


	@api.multi
	@api.model
	def dispatch(self):
		print"--------self._context------",self._context
		_logger.debug("Debug message",self._context)
		return {
			'name':   ('Dispatch'),
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'dispatch.wizard',
			'context':self._context,
			#'domain':[('id','in',ids)],
			'type': 'ir.actions.act_window',
			'target': 'new',
			'flags': {'form': {'action_buttons': True}}
		}
		'''
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
			#'total_grwt': self.total_grwt,
			#'total_ntwt': self.total_ntwt,
			#'total_vol': self.total_vol,
			'inv_id': self.id,
			'carrier_id': self.carrier_id and self.carrier_id.id or '',
			'incoterms': self.incoterms and self.incoterms.id or '',
			'target_year': self.target_year and self.target_year.id or '',
		}
		pack = self.env['packing.list'].create(vals)
		for line in self.invoice_line_ids:
			li = {'packing_line_ids':  [(0,0, {
				'product_id': line.product_id.id,
				'name': line.name,
				'order_qty': line.quantity,
				'quantity': line.quantity,
				'uom_id': line.uom_id.id,
			})],}
			pack.write(li)
		self.packing_flag = True
		self.packing_invoice_id = pack.id
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
			#'total_grwt': self.total_grwt,
			#'total_cartons': self.total_ntwt,
			'freight_charge': self.freight_charge,
			'freight_only': self.freight_only,
			'insur_charge': self.insurance_only,
			'bank_charge': self.bank_charge,
			'ext_charge': self.ext_charge,
			'global_disc': self.global_disc,
			'grand_total': self.amount_total,
			'inv_id': self.id,
			'packing_invoice_id': self.packing_invoice_id and self.packing_invoice_id.id or '',
		}
		export = self.env['export.invoice'].create(vals)
		for line in self.invoice_line_ids:
			li = {'export_line_ids':  [(0,0, {
				'product_id': line.product_id.id,
				'name': line.name,
				'order_qty': line.quantity,
				'quantity': line.quantity,
				'uom_id': line.uom_id.id,
				'price_unit1': line.price_unit,
				'price_unit': line.price_unit,
				'discount': self.global_disc / len(self.invoice_line_ids),
				'price_subtotal': line.quantity  * line.price_unit,
			})],}
			export.write(li)
		self.export_flag = True
		self.export_invoice_id = export.id
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


	@api.onchange('company_id')
	def onchange_company(self):
		print"---------self-----new--company---",self,self.company_id
		packing_ids = self.env['packing.list'].search([('inv_id','=',self._origin.id)])
		if packing_ids:
			for packing_id in packing_ids:
				packing_id.write({'company_id':self.company_id.id})

	@api.onchange('inv_no','date_invoice','pre_carrier','origin_country','flight_no', 'port_discharge', 'dest_country', 'port_discharge', 'final_dest','pl_receipt','port_loading')
	def onchange_invoice_no(self):
		print"---------self-----inv-date--",self,self.inv_no
		packing_ids = self.env['packing.list'].search([('inv_id','=',self._origin.id)])
		if packing_ids:
			for packing_id in packing_ids:
				packing_id.write({'inv_no':self.inv_no, 'date_invoice': self.date_invoice, 'pre_carrier': self.pre_carrier, 'origin_country': self.origin_country,
					'flight_no': self.flight_no, 'port_discharge': self.port_discharge, 'dest_country': self.dest_country and self.dest_country.name, 
					'port_discharge': self.port_discharge, 'final_dest': self.final_dest,'pl_receipt': self.pl_receipt, 'port_loading': self.port_loading,
				})


	@api.onchange('payment_term_id')
	def change_payment_term(self):
		print"-----change_payment_term----sel;f=======",self.payment_term_id
		packing_ids = self.env['packing.list'].search([('inv_id','=',self._origin.id)])
		if packing_ids:
			for packing_id in packing_ids:
				packing_id.write({'payment_term_id':self.payment_term_id.id})

class AccountInvoiceLine(models.Model):
	_inherit = "account.invoice.line"

	order_qty = fields.Float('Order Qty')
	hsn_code = fields.Many2one('hsn.tax',string='HS Code')

class DispatchWiz(models.TransientModel):
	_name = "dispatch.wizard"

	date = fields.Date("Dispatch Date", required=True)

	@api.multi
	@api.model
	def submit(self):
		_logger.debug("Debug message",self._context)
		print"------------self------subit---",self._context
		if self._context:
			#invoice_id = self.env['account.invoice'].search([('id','=',self._context['params']['id'])])
			invoice_id = self.env['account.invoice'].search([('id','=',self._context['active_id'])])
			print"---------invoice_id-------",invoice_id
			_logger.debug("Debug message",invoice_id)
			for invoice in invoice_id:
				invoice.dispatched_date = self.date
				invoice.hide_dispatch = True
				invoice.state = 'dispatch'
				orders = self.env['sale.order'].search([('name','=',invoice.origin)])
				for order in orders:
					print"----------",order
					order.state = 'dispatched'
					order.invoice_status = 'dispatched'

				purchase_order = self.env['purchase.order'].search([('origin','like',invoice.origin)])
				for po in purchase_order:
					print"----------",po
					po.bill_no = invoice.inv_no
					po.inv_date = invoice.date_invoice
					po.bill_date = self.date
				sale_mis = self.env['mis.reporting'].search([('order_id.name','=',invoice.origin)])
				for mis in sale_mis:
					print"----------",mis
					mis.invoice = invoice.inv_no
					mis.dispatch_date = self.date

				purchase_mis = self.env['po_mis.reporting'].search([('po_no.name','=',invoice.origin)])
				for pomis in purchase_mis:
					print"----------",pomis
					pomis.invoice = invoice.inv_no
					pomis.invoice_date = invoice.date_invoice
					pomis.invoice_val = invoice.amount_total
				
				year = ''
				month = ''
				if invoice.date_invoice:
					year = datetime.datetime.strptime(invoice.date_invoice, '%Y-%m-%d').strftime('%Y')
					month = datetime.datetime.strptime(invoice.date_invoice, '%Y-%m-%d').month
					if month <= 3:
						financial_year = self.env['fin.year'].search([('name','like', '-'+str(year[2:]))])
					if month > 3:
						financial_year = self.env['fin.year'].search([('name','ilike', year)], limit=1)
					financial_year = financial_year.id

				executed_sales = self.env['old.export']
				shipping_panel = self.env['shipping.panel']
				executed_val = {'partner_id': invoice.partner_id.id, 'consignee': invoice.consignee and invoice.consignee.id or '', 'notify': invoice.partner_id.id, 'country_id': invoice.partner_id.country_id.id, 'pl_receipt': invoice.pl_receipt, 'origin_country': invoice.origin_country,
								'exporter_id': invoice.company_id.id, 'payment_term_id': invoice.payment_term_id.id, 'destination_country': invoice.dest_country and invoice.dest_country.id or '', 'total_grwt': invoice.total_grwt, 'total_ntwt': invoice.total_ntwt, 'total_vol_manuall': invoice.packing_invoice_id.total_vol_manuall, 'vol_unit': invoice.packing_invoice_id.vol_unit and invoice.packing_invoice_id.vol_unit.id or '',
								'incoterm_id': orders.incoterms.id, 'order_no': invoice.origin, 'order_date': invoice.order_date,
								'name': invoice.inv_no, 'date_invoice': invoice.date_invoice, 'financial_year': financial_year, 'mkt_coordinator': invoice.user_id.id,
								'carrier_id': orders.carrier_id.id, 'dest_country': invoice.dest_country.name, 'amount': invoice.amount_total,
								'port_loading': invoice.port_loading, 'port_discharge': invoice.port_discharge,'dispatched_date': self.date
				}	
				executed_sales_id = executed_sales.create(executed_val)
				shipping_panel_val = {
										'partner_id': invoice.partner_id.id, 
										'country_id': invoice.partner_id.country_id.id, 									
										'exporter_id': invoice.company_id.id, 
										'carrier_id': invoice.carrier_id.id or '',
										'incoterm_id': orders.incoterms.id, 
										'order_no': invoice.origin, 
										'order_date': invoice.order_date,
										'name': invoice.inv_no, 
										'date_invoice': invoice.date_invoice, 			
										'financial_year':financial_year, 
										'mkt_coordinator': invoice.user_id.id, 
										'old_export_id': executed_sales_id.id, 
										'amount': invoice.amount_total,
				}	
				shipping_panel_id = shipping_panel.create(shipping_panel_val)
				print"----executed_sales_id-----shipping_panel--",executed_sales_id,shipping_panel_id
