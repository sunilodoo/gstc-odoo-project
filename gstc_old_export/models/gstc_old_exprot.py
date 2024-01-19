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

	name = fields.Char('Inv No.')
	exporter_id = fields.Many2one('res.company', string='Shipper')
	partner_id = fields.Many2one("res.partner", string="Customer")	
	order_no = fields.Char("P.I(SO No.)")
	order_date = fields.Date("P.I(SO Date)")
	country_id = fields.Many2one('res.country', string='Country')
	company_id = fields.Many2one('res.company', string='Company')
	mkt_coordinator = fields.Many2one('res.users', string="Mkt Coord")
	dest_country = fields.Char(string="Final Destination",)
	origin_country = fields.Char('Country of Origin')
	destination_country = fields.Many2one('res.country', string='Country of Dest.')
	date_invoice = fields.Date('Inv Date')
	amount = fields.Float("Inv Val(USD)")
	exchange_rate = fields.Float("Exchange Rate")
	payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms')
	incoterm_id = fields.Many2one('incoterm.trade', string='Incoterms')
	carrier_id = fields.Many2one('delivery.carrier', string='MoS')	
	port_loading = fields.Char('PoL')
	port_discharge = fields.Char('PoD')
	amount_inr = fields.Float("Payment Real.(INR)")
	actual_sale_inr = fields.Float(compute='compute_inr_total', string='Actual Sale amt(INR)', store=True)
	export_image = fields.Many2many('ir.attachment', 'export_attachments_rel',
        'export_id', 'attachment_id', string='Attachments')
	financial_year = fields.Many2one('fin.year', string='Financial Year')
	#new field added from here
	consignee = fields.Many2one('res.partner', string="Consignee")
	notify = fields.Many2one('res.partner', string="Notify")
	total_grwt = fields.Float(string='Gross Weight')
	total_ntwt = fields.Float(string='Net Weight')
	total_carton = fields.Float(string='Total Carton')
	total_vol_manuall = fields.Float(string='Volume Weight')
	vol_unit = fields.Many2one('product.uom', string='Unit', copy=True)
	pl_receipt = fields.Char('Place of Receipt', copy=True)
	dispatched_date = fields.Date('Dispatch Date')
	stuffing_date = fields.Date('Stuffing Date')
	railing_date = fields.Date('Railing Date')
	container_no = fields.Char('Container Number')
	custom_seal_no = fields.Char('Custom Seal No.')
	line_seal_no = fields.Char('Line Seal No.')
	agency_seal_no = fields.Char('Inspection Agency Seal Number')
	ship_airline_name = fields.Char('Shipping/Air Line Name')
	vessel_flight_name = fields.Char('Vessel/Flight Name')
	ship_onboard_airlift_date = fields.Date('Ship on Board/Air Lift Date')
	port_arrival_date = fields.Date('Transhipment Port Arrival Date')
	port_vessel_flight_name = fields.Char('Transhipment Port Vessel / Flight Name')
	port_onboard_airlift_date = fields.Date('Transhipment Port Ship on Board/Air Lift Date')
	discharge_eta_date = fields.Date('Port of Discharge (ETA/ATA) Date')
	destination_eta_date = fields.Date('Final Destination  (ETA/ATA) Date')
	do_delivery_date = fields.Date('D.O Delivery Date')	
	remarks = fields.Text('Remarks')
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
	clearance_subtotal_fee = fields.Float(compute='compute_clearace_total', string='Total(Without Tax)', store=True)
	clearance_tax_fee = fields.Float('Tax')
	clearance_total_fee = fields.Float(compute='compute_clearace_total', string='Total(With Tax)', store=True)
	clearance_remarks = fields.Text("Remarks")
	#SHIPPING LINE CHARGES
	shipping_line_charges = fields.One2many('shipping.line.charges', 'export_id', string="FORWARDERS / SHIPPING LINE CHARGES") 
	#OTHER CHARGES
	other_transport_fee = fields.Float('Origin Transportation')
	other_ihc_fee = fields.Float('PDA (IHC)')
	other_certificate_fee = fields.Float('Certificate of Origin Fee')
	other_inspection_fee = fields.Float('Inspection Fee')
	other_misc_fee = fields.Float('Miscellaneous Charges')
	other_insurance = fields.Float('Insurance')
	other_subtotal_fee = fields.Float(compute='compute_other_total', string='Total(without Tax)', store=True)
	other_tax_fee = fields.Float('Tax')
	other_total_fee = fields.Float(compute='compute_other_total', string='Total(with Tax)', store=True)
	other_remarks = fields.Text("Remarks")

	total_purchase = fields.Float('Total Purchase')
	lc_banking_cost = fields.Float('LC/Banking cost')
	shippig_cost = fields.Float(compute='compute_shipping_cost', string='Shipping Cost', store=True)
	packing_cost = fields.Float('Packing Cost')
	commission = fields.Float('Commission(%)')
	commission_amt = fields.Float(string='Commission Amount')
	# commission_amt = fields.Float(compute='compute_gross_margin', string='Commission Amount', store=True)
	total_gross_margin = fields.Float(compute='compute_gross_margin', string='G.M', store=True)
	total_gross_percent = fields.Float(compute='compute_gross_margin', string='G.M %', store=True)
	difference_in_sale = fields.Float(compute='compute_difference', string='Realized Diff.', store=True)


	active = fields.Boolean(
        'Active', default=True,
        help="If unchecked, it will allow you to hide the PO without removing it.")


	@api.depends('amount','exchange_rate')
	def compute_inr_total(self):
		for rec in self:
			val = rec.amount * rec.exchange_rate
			rec.actual_sale_inr = val


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

	@api.onchange('amount_inr', 'commission')
	def onchange_for_mg(self):
		commission_amt = self.amount_inr*self.commission/100
		self.update({'commission_amt': commission_amt})
		
	@api.depends('amount_inr', 'total_purchase','lc_banking_cost','shippig_cost','packing_cost','commission', 'commission_amt')
	def compute_gross_margin(self):
		for rec in self:
			commission_amt = rec.amount_inr*rec.commission/100
			gross = rec.amount_inr - rec.total_purchase - rec.lc_banking_cost - rec.shippig_cost - rec.packing_cost - rec.commission_amt
			rec.total_gross_margin = gross
			if rec.amount_inr > 0:
				gm = gross/rec.amount_inr*100
				rec.total_gross_percent = gm
	# @api.depends('total_purchase','lc_banking_cost','shippig_cost','packing_cost','commission')
	# def compute_gross_margin(self):
	# 	for rec in self:
	# 		gross = rec.amount_inr - rec.total_purchase - rec.lc_banking_cost - rec.shippig_cost - rec.packing_cost
	# 		gross1 = gross - (gross * rec.commission)/100
	# 		rec.total_gross_margin = gross1
	# 		if rec.amount_inr > 0:
	# 			gm = gross1/rec.amount_inr*100
	# 			rec.total_gross_percent = gm

	@api.depends('clearance_total_fee','shipping_line_charges.shipping_total_fee','other_total_fee')
	def compute_shipping_cost(self):
		for rec in self:
			shipping = rec.clearance_total_fee + sum(l.shipping_total_fee for l in rec.shipping_line_charges) + rec.other_total_fee
			rec.shippig_cost = shipping

	@api.depends('amount_inr','actual_sale_inr')
	def compute_difference(self):
		for rec in self:
			diff = rec.amount_inr - rec.actual_sale_inr
			rec.difference_in_sale = diff

	@api.multi
	def payment_difference(self):
		for rec in self.search([]):
			diff = rec.amount_inr - rec.actual_sale_inr
			rec.difference_in_sale = diff

	@api.depends('service_charge','shipping_process_fee','measurement_fee','load_upload_fee','adc_noc_fee','challan_penalty_fee','clearance_misc_fee','clearance_tax_fee')
	# @api.depends('service_charge','shipping_process_fee','measurement_fee','load_upload_fee','adc_noc_fee','challan_penalty_fee','clearance_misc_fee','clearance_subtotal_fee','clearance_tax_fee')
	def compute_clearace_total(self):
		for rec in self:
			total = rec.service_charge + rec.shipping_process_fee + rec.measurement_fee+ rec.load_upload_fee + rec.adc_noc_fee + rec.challan_penalty_fee + rec.clearance_misc_fee
			rec.clearance_subtotal_fee = total
			tax = rec.clearance_tax_fee
			rec.clearance_total_fee = total + tax

	@api.depends('other_transport_fee','other_ihc_fee','other_certificate_fee','other_inspection_fee','other_misc_fee','other_insurance', 'other_tax_fee')
	# @api.depends('other_transport_fee','other_ihc_fee','other_certificate_fee','other_inspection_fee','other_misc_fee','other_insurance','other_subtotal_fee','other_tax_fee')
	def compute_other_total(self):
		for rec in self:
			total = rec.other_transport_fee + rec.other_ihc_fee + rec.other_certificate_fee+ rec.other_inspection_fee + rec.other_misc_fee + rec.other_insurance
			rec.other_subtotal_fee = total
			tax = rec.other_tax_fee
			rec.other_total_fee = total + tax

	@api.model
	def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
		result = super(OldExport, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)
		if 'total_gross_margin' in fields and 'amount_inr' in fields :
			for rec in result:
				if rec['amount_inr'] > 0 and rec['total_gross_margin'] > 0:
					rec['total_gross_percent'] = (rec['total_gross_margin'] /rec['amount_inr']) * 100
		if 'exchange_rate' in fields:
			for rec in result:
				if rec['amount'] > 0 and rec['actual_sale_inr'] > 0 and rec['exchange_rate'] > 0:
					print"===result==",result
					rec['exchange_rate'] = rec['actual_sale_inr']/rec['amount']
		return result
	
	@api.multi
	def update_shipping_panel(self):
		vals = []
		for rec in self.search([('active','=',True)]):
			shipping_panel_line = self.env['shipping.panel.line']
			shipping_panel = self.env['shipping.panel'].search([('old_export_id','=',rec.id)])
			if shipping_panel:
				# DOCUMENTAION TAB
				shipping_panel.shipping_bill_no = rec.shipping_bill_no
				shipping_panel.shipping_bill_date = rec.shipping_bill_date
				shipping_panel.port_code = rec.port_code
				shipping_panel.drawback_amount = rec.drawback_amount
				shipping_panel.bl_awb_no = rec.bl_awb_no
				shipping_panel.bl_awb_date = rec.bl_awb_date
				shipping_panel.document_send_date = rec.document_send_date
				shipping_panel.document_tracking_no = rec.document_tracking_no
				shipping_panel.courier_name = rec.courier_name
				shipping_panel.document_delvy_date = rec.document_delvy_date
				#CLEARANCE CHARGES
				shipping_panel.cha_name = rec.cha_name
				shipping_panel.service_charge = rec.service_charge
				shipping_panel.shipping_process_fee = rec.shipping_process_fee
				shipping_panel.measurement_fee = rec.measurement_fee
				shipping_panel.load_upload_fee = rec.load_upload_fee
				shipping_panel.adc_noc_fee = rec.adc_noc_fee
				shipping_panel.challan_penalty_fee = rec.challan_penalty_fee
				shipping_panel.clearance_misc_fee = rec.clearance_misc_fee
				shipping_panel.clearance_total_fee = rec.clearance_total_fee
				shipping_panel.clearance_remarks = rec.clearance_remarks
				#OTHER CHARGES
				shipping_panel.other_transport_fee = rec.other_transport_fee
				shipping_panel.other_ihc_fee = rec.other_ihc_fee
				shipping_panel.other_certificate_fee = rec.other_certificate_fee
				shipping_panel.other_inspection_fee = rec.other_inspection_fee
				shipping_panel.other_misc_fee = rec.other_misc_fee
				shipping_panel.other_insurance = rec.other_insurance
				shipping_panel.other_total_fee = rec.other_total_fee
				shipping_panel.other_remarks = rec.other_remarks
			#SHIPPING LINE CHARGES
			print"-----------self---change_year-------",rec
			for line in rec.shipping_line_charges:
				print"--shipping_panel_line-------",line
				shipping_panel_line = self.env['shipping.panel.line'].search([('line_charges_id','=',line.id)])
				if not shipping_panel_line:
					vals = {'shipping_panel_line':  [(0,0, {
						'name': line.name,
						'line_charges_id': line.id,
						'freight': line.freight,
						'on_carriage': line.on_carriage,
						'thc_fee': line.thc_fee,
						'ihc_fee': line.ihc_fee,
						'bl_awb_fee': line.bl_awb_fee,
						'vgm_ens_fee': line.vgm_ens_fee,
						'tc_reciept_fee': line.tc_reciept_fee,
						'custom_duty_fee': line.custom_duty_fee,
						'dest_exp_fee': line.dest_exp_fee,
						'transport_fee': line.transport_fee,
						'shipping_misc_fee': line.shipping_misc_fee,
						'shipping_remarks': line.shipping_remarks,
						
					})],}
					shipping_panel.write(vals)
				if shipping_panel_line:
					shipping_panel_line.update({
						'name': line.name,
						'line_charges_id': line.id,
						'freight': line.freight,
						'on_carriage': line.on_carriage,
						'thc_fee': line.thc_fee,
						'ihc_fee': line.ihc_fee,
						'bl_awb_fee': line.bl_awb_fee,
						'vgm_ens_fee': line.vgm_ens_fee,
						'tc_reciept_fee': line.tc_reciept_fee,
						'custom_duty_fee': line.custom_duty_fee,
						'dest_exp_fee': line.dest_exp_fee,
						'transport_fee': line.transport_fee,
						'shipping_misc_fee': line.shipping_misc_fee,
						'shipping_remarks': line.shipping_remarks,
					})

	@api.multi
	@api.model
	def create_shipping_panel(self):
		vals = []
		for rec in self.search([('active','=',True)]):
			shipping_panel = self.env['shipping.panel'].search([('old_export_id','=',rec.id)])
			if not shipping_panel:
				shipping_panel_val = {
										'partner_id': rec.partner_id.id, 
										'country_id': rec.partner_id.country_id.id, 									
										'exporter_id': rec.company_id.id, 
										'carrier_id': rec.carrier_id.id or '',
										'incoterm_id': rec.incoterm_id.id, 
										'order_no': rec.order_no, 
										'order_date': rec.order_date,
										'name': rec.name, 
										'date_invoice': rec.date_invoice, 			
										'financial_year': rec.financial_year.id, 
										'mkt_coordinator': rec.mkt_coordinator.id, 
										'amount': rec.amount,
										'old_export_id': rec.id
				}	
				shipping_panel_id = self.env['shipping.panel'].create(shipping_panel_val)
				print"--------shipping_panel--",shipping_panel_id

			
class ShippingLineCharges(models.Model):
	_name = "shipping.line.charges"


	@api.depends('freight','on_carriage','thc_fee','ihc_fee','bl_awb_fee','vgm_ens_fee','tc_reciept_fee','custom_duty_fee','dest_exp_fee','transport_fee','shipping_misc_fee','shipping_subtotal_fee','shipping_tax_fee')
	def compute_total(self):
		total = 0
		for rec in self:
			total = rec.freight + rec.on_carriage + rec.thc_fee + rec.ihc_fee + rec.bl_awb_fee + rec.vgm_ens_fee + rec.tc_reciept_fee + rec.custom_duty_fee + rec.dest_exp_fee + rec.transport_fee + rec.shipping_misc_fee
			rec.shipping_subtotal_fee = total
			tax = rec.shipping_tax_fee
			rec.shipping_total_fee = total + tax

	export_id = fields.Many2one('old.export', string="Export ID")
	name = fields.Char('Name of Forwarder', required=True)
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
