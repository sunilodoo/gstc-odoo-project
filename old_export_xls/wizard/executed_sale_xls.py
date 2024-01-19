# -*- coding: utf-8 -*-
import xlwt
import base64
import calendar
from io import StringIO
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
from datetime import datetime

class ExecutedSaleXLS(models.TransientModel):
	_name = "executed.sale.excel"

	start_date = fields.Date(string='Start Date', required=True, default=datetime.today().replace(day=1))
	end_date = fields.Date(string="End Date", required=True, default=datetime.now().replace(day = calendar.monthrange(datetime.now().year, datetime.now().month)[1]))
	executed_data = fields.Char('Name', size=256)
	file_name = fields.Binary('Product Report', readonly=True)
	state = fields.Selection([('choose', 'choose'), ('get', 'get')],
                             default='choose')

	_sql_constraints = [
		('check','CHECK((start_date <= end_date))',"End date must be greater then start date")  
	]

	def get_pro_sale(self):
		final = []
		result = []
		final4 = []
		current_day = datetime.today().day
		total_order = self.env['old.export'].search([('date_invoice','>=',self.start_date),('date_invoice','<=',self.end_date),('active','=',True)])
		for line in total_order:
			result.append({'shipper':line.exporter_id and (line.exporter_id.name) or '', 'customer':line.partner_id and (line.partner_id.name) or '', 'country': line.country_id and line.country_id.name or '', 'consignee': line.consignee and line.consignee.name or '', 'notify': line.notify and line.notify.name or '', 'payment_terms': line.payment_term_id and line.payment_term_id.name or '', 'shipment_mode': line.carrier_id and line.carrier_id.name or '', 'incoterms': line.incoterm_id and line.incoterm_id.name or '', 'user_id': line.mkt_coordinator and line.mkt_coordinator.name or '', 'order_no': line.order_no, 'order_date': line.order_date, 'name': line.name, 'inv_date': line.date_invoice, 'financial_year': line.financial_year and line.financial_year.name, 'currency': line.partner_id.property_product_pricelist and line.partner_id.property_product_pricelist.currency_id.name, 'amount': line.amount, 'conversion_rate': line.exchange_rate, 'actual_sale_inr': line.actual_sale_inr, 'amount_inr': line.amount_inr, 'difference_in_sale': line.difference_in_sale, 'total_purchase': line.total_purchase, 'lc_banking_cost': line.lc_banking_cost, 'shipping_cost': line.shippig_cost, 'packing_cost': line.packing_cost, 'commission': line.commission, 'total_gross_margin': line.total_gross_margin, 'total_gross_percent': line.total_gross_percent, 'total_grwt': line.total_grwt, 'total_ntwt': line.total_ntwt, 'total_vol_manuall': line.total_vol_manuall, 'origin_country': line.origin_country, 'destination_country': line.destination_country and line.destination_country.name or '', 'dest_country': line.dest_country, 'destination_eta_date': line.destination_eta_date, 'port_loading': line.port_loading, 'pl_receipt': line.pl_receipt and line.pl_receipt or '', 'dispatched_date': line.dispatched_date, 'port_discharge': line.port_discharge, 'discharge_eta_date': line.discharge_eta_date, 'port_code': line.port_code, 'shipping_bill_no': line.shipping_bill_no, 'shipping_bill_date': line.shipping_bill_date, 'drawback_amount': line.drawback_amount})

		final = sorted(result, key=lambda k: k['name'])
	
		

		print"-------sale_order------",final
		final_value = {}
		order_lines = []
		workbook = xlwt.Workbook()
		sheet = workbook.add_sheet('Executed Sale Details',cell_overwrite_ok=True)
		final_value['start_date'] = self.start_date
		final_value['end_date'] = self.end_date
		format0 = xlwt.easyxf('font:height 500,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center')
		format1 = xlwt.easyxf('font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz left')
		format2 = xlwt.easyxf('font:bold True;align: horiz left')
		format3 = xlwt.easyxf('align: horiz left')
		format4 = xlwt.easyxf('align: horiz right')
		format5 = xlwt.easyxf('font:bold True;align: horiz right')
		format6 = xlwt.easyxf('font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz right')
		format7 = xlwt.easyxf('font:bold True;borders:top thick;align: horiz right')
		format8 = xlwt.easyxf('font:bold True;borders:top thick;pattern: pattern solid, fore_colour gray25;align: horiz left')

		sheet.col(0).width = int(30*260)
		sheet.col(1).width = int(30*260)    
		sheet.col(2).width = int(18*260)    
		sheet.col(3).width = int(18*260) 
		sheet.col(4).width = int(15*260)   
		sheet.col(5).width = int(15*260)
		sheet.col(6).width = int(33*260)   
		sheet.write_merge(0, 2, 0, 7, 'Executed Sale Report', format0)
		sheet.write(3, 0, "Start Date", format1)
		sheet.write(3, 1, final_value['start_date'], format3)
		sheet.write(3, 2, "End Date", format1)
		sheet.write(3, 3, final_value['end_date'], format3)

		sheet.write(5, 0, 'Shipper', format1)
		sheet.write(5, 1, 'Customer', format1)
		sheet.write(5, 2, 'Country', format1)
		sheet.write(5, 3, 'Consignee', format1)
		sheet.write(5, 4, 'Notify', format1)
		sheet.write(5, 5, 'Payment Terms', format6)
		sheet.write(5, 6, 'Mode of Shipment', format1)
		sheet.write(5, 7, 'Incoterms', format6)
		sheet.write(5, 8, 'Mkt Coordinator', format6)
		sheet.write(5, 9, 'P.I(SO No.) ', format6)
		sheet.write(5, 10, 'P.I(SO Date) ',format6)
		sheet.write(5, 11, 'Inv No.',format6)
		sheet.write(5, 12, 'Inv Date',format6)
		sheet.write(5, 13, 'Financial Year',format6)
		sheet.write(5, 14, 'Currency',format6)
		sheet.write(5, 15, 'Inv Val(USD)',format6)
		sheet.write(5, 16, 'Conversion Rate',format6)
		sheet.write(5, 17, 'Actual Sale amt(INR)',format6)
		sheet.write(5, 18, 'Payment Real.(INR) ',format6)
		sheet.write(5, 19, 'Realized Diff.',format6)
		sheet.write(5, 20, 'Total Purchase ',format6)
		sheet.write(5, 21, 'LC/Banking cost',format6)

		sheet.write(5, 22, 'Shipping Cost ', format1)
		sheet.write(5, 23, 'Packing Cost', format1)
		sheet.write(5, 24, 'Commission(%)', format1)
		sheet.write(5, 25, 'G.M', format1)
		sheet.write(5, 26, 'G.M %', format1)
		sheet.write(5, 27, 'Gross Weight', format6)
		sheet.write(5, 28, 'Net Weight ', format1)
		sheet.write(5, 29, 'Volume Weight', format6)
		sheet.write(5, 30, 'Country of Origin', format6)
		sheet.write(5, 31, 'Country of Dest. ', format6)
		sheet.write(5, 32, 'Final Destination ',format6)
		sheet.write(5, 33, 'Final Destination (ETA/ATA) Date ',format6)
		sheet.write(5, 34, 'PoL',format6)
		sheet.write(5, 35, 'Place of Receipt',format6)
		sheet.write(5, 36, 'Dispatch Date ',format6)
		sheet.write(5, 37, 'PoD',format6)
		sheet.write(5, 38, 'Port of Discharge (ETA/ATA) Date ',format6)

		sheet.write(5, 39, 'Port Code',format6)
		sheet.write(5, 40, 'Shipping Bill No. ',format6)
		sheet.write(5, 41, 'Shipping Bill Date ',format6)
		sheet.write(5, 42, 'Drawback Amount ',format6)

		row = 6 
		total_qty_pcs = 0.00
		total_price_pcs = 0.00               
		for rec in final:
			sheet.write(row, 0, rec.get('shipper'), format3)
			sheet.write(row, 1, rec.get('customer'), format3)
			sheet.write(row, 2, rec.get('country'), format3)
			sheet.write(row, 3, rec.get('consignee'), format3)
			sheet.write(row, 4, rec.get('notify'), format4)
			sheet.write(row, 5, rec.get('payment_terms'), format4)
			sheet.write(row, 6, rec.get('shipment_mode'), format4)
			sheet.write(row, 7, rec.get('incoterms'), format4)
			sheet.write(row, 8, rec.get('user_id'), format4)
			sheet.write(row, 9, rec.get('order_no'), format4)
			sheet.write(row, 10, rec.get('order_date'), format4)
			sheet.write(row, 11, rec.get('name'), format4)
			sheet.write(row, 12, rec.get('inv_date'), format4)
			sheet.write(row, 13, rec.get('financial_year'), format4)
			sheet.write(row, 14, rec.get('currency'), format4)
			sheet.write(row, 15, rec.get('amount'), format4)
			sheet.write(row, 16, rec.get('conversion_rate'), format4)
			sheet.write(row, 17, rec.get('actual_sale_inr'), format4)
			sheet.write(row, 18, rec.get('amount_inr'), format4)
			sheet.write(row, 19, rec.get('difference_in_sale'), format4)
			sheet.write(row, 20, rec.get('total_purchase'), format4)
			sheet.write(row, 21, rec.get('lc_banking_cost'), format4)

			sheet.write(row, 22, rec.get('shipping_cost'), format3)
			sheet.write(row, 23, rec.get('packing_cost'), format3)
			sheet.write(row, 24, rec.get('commission'), format3)
			sheet.write(row, 25, rec.get('total_gross_margin'), format3)
			sheet.write(row, 26, rec.get('total_gross_percent'), format4)
			sheet.write(row, 27, rec.get('total_grwt'), format4)
			sheet.write(row, 28, rec.get('total_ntwt'), format4)
			sheet.write(row, 29, rec.get('total_vol_manuall'), format4)
			sheet.write(row, 30, rec.get('origin_country'), format4)
			sheet.write(row, 31, rec.get('destination_country'), format4)
			sheet.write(row, 32, rec.get('dest_country'), format4)
			sheet.write(row, 33, rec.get('destination_eta_date'), format4)
			sheet.write(row, 34, rec.get('port_loading'), format4)
			sheet.write(row, 35, rec.get('pl_receipt'), format4)
			sheet.write(row, 36, rec.get('dispatched_date'), format4)
			sheet.write(row, 37, rec.get('port_discharge'), format4)
			sheet.write(row, 38, rec.get('discharge_eta_date'), format4)

			sheet.write(row, 39, rec.get('port_code'), format4)
			sheet.write(row, 40, rec.get('shipping_bill_no'), format4)
			sheet.write(row, 41, rec.get('shipping_bill_date'), format4)
			sheet.write(row, 42, rec.get('drawback_amount'), format4)

			row += 1
			#total_qty_pcs = total_qty_pcs + rec.get('qty_total')
			#total_price_pcs = total_price_pcs + rec.get('price_pcs')
		row += 2
		filename = ('Executed Sale Report'+ '.xls')
		workbook.save('/home/odoo/workspace/odoo10'+filename)
		file = open('/home/odoo/workspace/odoo10'+filename, "rb")
		#workbook.save(filename)
		#file = open(filename, "rb")
		file_data = file.read()
		out = base64.encodestring(file_data)
		self.write({'state': 'get', 'file_name': out, 'executed_data':'Executed Sale Report.xls'})
		return {
			'type': 'ir.actions.act_window',
			'res_model': 'executed.sale.excel',
			'view_mode': 'form',
			'view_type': 'form',
			'res_id': self.id,
			'target': 'new',
		}          
