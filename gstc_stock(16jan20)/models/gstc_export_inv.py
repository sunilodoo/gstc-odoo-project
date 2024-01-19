# -*- coding: utf-8 -*-

from odoo import models, fields, osv, api, _
from odoo.tools.translate import _
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import Warning, UserError
from datetime import timedelta
import datetime
from odoo.tools import amount_to_text_en, float_round
import num2words

class ExportInvoice(models.Model):
	_name = "export.invoice"

	@api.one
	@api.depends('export_line_ids.price_subtotal')
	def _compute_amount(self):
		self.amount_untaxed = sum(line.price_subtotal for line in self.export_line_ids)

	@api.multi    
	def amount_to_text(self, amount):
		convert_amount_in_words = num2words.num2words(amount, lang='en_IN')
		convert_amount_in_words = convert_amount_in_words.replace(' and','').replace(' point', ' Rupees and ')         
		return convert_amount_in_words

	name = fields.Char('Name')
	origin = fields.Char('Source Document')
	company_id = fields.Many2one('res.company', string='Company')
	partner_id = fields.Many2one("res.partner", string="Customer")	
	is_consignee = fields.Boolean('Inv to consignee')
	consignee = fields.Many2one('res.partner', string='Consignee')
	payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms')
	date_invoice = fields.Date('Invoice Date')
	conversion_rate = fields.Float('Conversion Rate')
	currency_id = fields.Many2one('res.currency', string='Currency')
	export_line_ids = fields.One2many('export.line', 'export_id', string='Export Lines')
	inv_no = fields.Char('Invoice No.')
	total_grwt = fields.Float('Gross Weight')
	total_cartons = fields.Float('Total Cartons')
	inv_id = fields.Many2one('account.invoice', string='Inv')
	amount_untaxed = fields.Monetary(string='Total Amount',
        store=True, readonly=True, compute='_compute_amount', track_visibility='always')
	freight_charge = fields.Monetary('Freight & Insurance')
	freight_only = fields.Float('Freight')
	insur_charge = fields.Float('Insurance')
	global_disc = fields.Monetary('Discount')
	bank_charge = fields.Monetary('Banking & Handling')
	ext_charge = fields.Monetary('Extra Charges')
	grand_total = fields.Monetary('Grand Total')
	reverse_charge = fields.Selection([('yes','Y'),('no','N')], default="no", string="Reverse Charge(Y/N)")
	datetime_supply = fields.Datetime('Date & Time of Supply')
	supply_place = fields.Char('Place of Supply')
	vehicle_no = fields.Char('Vehicle Number')
	lut_no = fields.Many2one('export.lut', string='Export Under LUT No.')
	eway_bill = fields.Char('E-Way Bill')
	transport_mode = fields.Char('Transport Mode')
	remarks = fields.Text('Remarks')
	sb_no = fields.Char('S.B No.')
	sb_date = fields.Date('S.B Date')
	declaration = fields.Text('Declaration')
	

	@api.model
	def create(self, vals):
		seq = self.env['ir.sequence'].next_by_code('export.invoice') or '/'
		vals['name'] = seq
		return super(ExportInvoice, self).create(vals)

	@api.onchange('conversion_rate','export_line_ids.price_unit','export_line_ids.price_subtotal')
	def _compute_convert_amount(self):
		if self and self.export_line_ids:
			for line in self.export_line_ids:
				if (self.conversion_rate > 0):
					line.price_unit = line.price_unit * self.conversion_rate
					line.discount = (self._origin.inv_id.global_disc / len(self._origin.inv_id.invoice_line_ids))* self.conversion_rate
					self.freight_charge = self._origin.inv_id.freight_charge * self.conversion_rate
					self.bank_charge = self._origin.inv_id.bank_charge * self.conversion_rate
					self.ext_charge = self._origin.inv_id.ext_charge * self.conversion_rate
					self.global_disc = self._origin.inv_id.global_disc * self.conversion_rate
					self.grand_total = (sum(line.price_subtotal for line in self.export_line_ids))  + (self._origin.inv_id.freight_charge * self.conversion_rate) + (self._origin.inv_id.bank_charge * self.conversion_rate) + (self._origin.inv_id.ext_charge * self.conversion_rate) - (self._origin.inv_id.global_disc * self.conversion_rate)
				else:
					print"---------------jfkdjf-----",self,self._origin,self.inv_id,self.inv_id.global_disc,len(self.inv_id.invoice_line_ids)
					line.price_unit = line.price_unit1
					line.discount = self._origin.inv_id.global_disc / len(self._origin.inv_id.invoice_line_ids)
					self.freight_charge = self._origin.inv_id.freight_charge 
					self.bank_charge = self._origin.inv_id.bank_charge 
					self.ext_charge = self._origin.inv_id.ext_charge
					self.global_disc = self._origin.inv_id.global_disc
					self.grand_total = sum(line.price_subtotal for line in self.export_line_ids) + self._origin.inv_id.freight_charge + self._origin.inv_id.bank_charge + self._origin.inv_id.ext_charge - self._origin.inv_id.global_disc
	
class ExportLine(models.Model):
	_name = "export.line"

	@api.one
	@api.depends('price_unit', 'quantity')
	def _compute_price(self):
		self.price_subtotal = self.quantity * self.price_unit

	export_id = fields.Many2one("export.invoice", string="Export ID")	
	#product_id = fields.Many2one('product.product', string='Product')
	name = fields.Char('Description', required=True)
	hsn = fields.Many2one('hsn.tax', string='HSN Code')
	quantity = fields.Float('Quantity')
	uom_id = fields.Many2one('product.uom', string='UoM')
	price_unit1 = fields.Float('Unit Price1')
	price_unit = fields.Float('Unit Price')
	discount = fields.Float('Discount')
	tax_id = fields.Many2many('account.tax', string='Tax')
	price_subtotal = fields.Float(string='Amount',
        store=True, readonly=True, compute='_compute_price')

class ExportLUT(models.Model):
	_name = "export.lut"

	name = fields.Char('Number')
	financial_year = fields.Many2one('fin.year', string='Financial Year')



