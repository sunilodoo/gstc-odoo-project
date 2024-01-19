# -*- coding: utf-8 -*-

from odoo import models, fields, osv, api, _
from odoo.tools.translate import _
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import Warning, UserError
from datetime import timedelta
import datetime

class OldExport(models.Model):
	_name = "old.export"
	_order = 'date_invoice desc'

	name = fields.Char('Invoice No.')
	exporter_id = fields.Many2one('res.company', string='Exporter')
	partner_id = fields.Many2one("res.partner", string="Buyer")	
	order_no = fields.Char("So No (P.I)")
	order_date = fields.Date("So Date")
	country_id = fields.Many2one('res.country', string='Country')
	company_id = fields.Many2one('res.company', string='Company')
	mkt_coordinator = fields.Many2one('res.users', string="Mkt Coordinator")
	dest_country = fields.Char(string="Final Destination",)
	date_invoice = fields.Date('Invoice Date')
	amount = fields.Float("Inv. Amt(USD)")
	payment_term_id = fields.Many2one('account.payment.term', string='Nature of Payment')
	incoterm_id = fields.Many2one('incoterm.trade', string='Incoterm')
	carrier_id = fields.Many2one('delivery.carrier', string='Mode of Ship.')	
	port_loading = fields.Char('Port of Loading')
	port_discharge = fields.Char('Port of Discharge')
	amount_inr = fields.Float("Payment Real.(INR)")
	export_image = fields.Many2many('ir.attachment', 'export_attachments_rel',
        'export_id', 'attachment_id', string='Attachments')
	financial_year = fields.Many2one('fin.year', string='Financial Year')
	active = fields.Boolean(
        'Active', default=True,
        help="If unchecked, it will allow you to hide the PO without removing it.")


	@api.onchange('date_invoice')
	def change_year(self):
		print"-----------self---change_year-------",self.date_invoice
		year = ''
		month = ''
		if self.date_invoice:
			year = datetime.datetime.strptime(self.date_invoice, '%Y-%m-%d').strftime('%Y')
			month = datetime.datetime.strptime(self.date_invoice, '%Y-%m-%d').month
			if month <= 3:
				financial_year = self.env['fin.year'].search([('name','like', '-'+str(year[2:]))])
			if month > 3:
				financial_year = self.env['fin.year'].search([('name','ilike', year)])
			self.financial_year = financial_year.id

