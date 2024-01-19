# -*- coding: utf-8 -*-

from odoo import models, fields, osv, api, _
from odoo.tools.translate import _
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import Warning, UserError
from datetime import timedelta
import datetime

class ShippingPanel(models.Model):
	_name = "shipping.panel"
	_order = 'date_invoice desc'

	name = fields.Char('Inv No.')
	exporter_id = fields.Many2one('res.company', string='Shipper')
	partner_id = fields.Many2one("res.partner", string="Customer")	
	order_no = fields.Char("P.I(SO No.)")
	order_date = fields.Date("P.I(SO Date)")
	country_id = fields.Many2one('res.country', string='Country')
	company_id = fields.Many2one('res.company', string='Company')
	mkt_coordinator = fields.Many2one('res.users', string="Mkt Coord")
	date_invoice = fields.Date('Inv Date')
	amount = fields.Float("Inv Val(USD)")
	incoterm_id = fields.Many2one('incoterm.trade', string='Incoterms')
	carrier_id = fields.Many2one('delivery.carrier', string='MoS')	
	financial_year = fields.Many2one('fin.year', string='Financial Year')
	old_export_id = fields.Many2one('old.export', string="Executed Sales")
	# DOCUMENTAION TAB
	shipping_bill_no = fields.Char('Shipping Bill No.')
	shipping_bill_date = fields.Date('Shipping Bill Date')
	port_code = fields.Char('Port Code')
	drawback_amount = fields.Float('Drawback Amount')
	bl_awb_no = fields.Char('BL/AWB Number')
	bl_awb_date = fields.Date('BL/AWB Date')
	document_send_date = fields.Date('Original Documents Sending Date')
	document_tracking_no = fields.Char('Original Documents Tracking Number')
	courier_name = fields.Char('Name of Courier')
	document_delvy_date = fields.Date('Original Documents Delivery Date')
	#CLEARANCE CHARGES
	cha_name = fields.Char('CHA Name')
	service_charge = fields.Float('Service Charge')
	shipping_process_fee = fields.Float('Shipping Bill Process Fee')
	measurement_fee = fields.Float('Measurement Fee')
	load_upload_fee = fields.Float('Loading/Unloading Fee')
	adc_noc_fee = fields.Float('ADC NOC Fee')
	challan_penalty_fee = fields.Float('Challan / Penalty')
	clearance_misc_fee = fields.Float('Miscellaneous Charges')
	clearance_subtotal_fee = fields.Float(string='Total(Without Tax)')
	clearance_tax_fee = fields.Float('Tax')
	clearance_total_fee = fields.Float(string='Total(with Tax)')
	clearance_remarks = fields.Text("Remarks")
	#SHIPPING LINE CHARGES
	shipping_panel_line = fields.One2many('shipping.panel.line', 'panel_id', string="FORWARDERS / SHIPPING LINE CHARGES") 
	#OTHER CHARGES
	other_transport_fee = fields.Float('Origin Transportation')
	other_ihc_fee = fields.Float('PDA (IHC)')
	other_certificate_fee = fields.Float('Certificate of Origin Fee')
	other_inspection_fee = fields.Float('Inspection Fee')
	other_misc_fee = fields.Float('Miscellaneous Charges')
	other_insurance = fields.Float('Insurance')
	other_subtotal_fee = fields.Float(string='Total(without Tax)')
	other_tax_fee = fields.Float('Tax')
	other_total_fee = fields.Float(string='Total(With Tax)')
	other_remarks = fields.Text("Remarks")

	shippig_cost = fields.Float(string='Shippig Cost')
	active = fields.Boolean(
        'Active', default=True,
        help="If unchecked, it will allow you to hide the PO without removing it.")


class ShippingPanelLine(models.Model):
	_name = "shipping.panel.line"


	@api.depends('freight','on_carriage','thc_fee','ihc_fee','bl_awb_fee','vgm_ens_fee','tc_reciept_fee','custom_duty_fee','dest_exp_fee','transport_fee','shipping_misc_fee','shipping_subtotal_fee','shipping_tax_fee')
	def compute_total(self):
		total = 0
		for rec in self:
			total = rec.freight + rec.on_carriage + rec.thc_fee + rec.ihc_fee + rec.bl_awb_fee + rec.vgm_ens_fee + rec.tc_reciept_fee + rec.custom_duty_fee + rec.dest_exp_fee + rec.transport_fee + rec.shipping_misc_fee
			rec.shipping_subtotal_fee = total
			tax = rec.shipping_tax_fee
			rec.shipping_total_fee = total + tax

	line_charges_id = fields.Many2one('shipping.line.charges', string="Export Line ID")
	panel_id = fields.Many2one('shipping.panel', string="Panel ID")
	name = fields.Char('Name of Forwarder')
	freight = fields.Float('Freight')
	on_carriage = fields.Float('On-Carriage')
	thc_fee = fields.Float('THC')
	ihc_fee = fields.Float('IHC')
	bl_awb_fee = fields.Float('BL/AWB Fee')
	vgm_ens_fee = fields.Float('VGM / Sole / ENS / Seal Fee')
	tc_reciept_fee = fields.Float('TC / Reciepted')
	custom_duty_fee = fields.Float('Custom Duty')
	dest_exp_fee = fields.Float('Destination Expenses')
	transport_fee = fields.Float('Destination Transportation')
	shipping_misc_fee = fields.Float('Miscellaneous Charges')
	shipping_subtotal_fee = fields.Float(compute='compute_total', string='Total(Without Tax)', store=True)
	shipping_tax_fee = fields.Float('Tax')
	shipping_total_fee = fields.Float(compute='compute_total', string='Total(With Tax)', store=True)
	shipping_remarks = fields.Text("Remarks")

