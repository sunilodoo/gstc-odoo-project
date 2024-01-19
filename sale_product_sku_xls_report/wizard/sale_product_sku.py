# -*- coding: utf-8 -*-
import xlwt
import base64
import calendar
from io import StringIO
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
from datetime import datetime

class SaleOrderExcelSKU(models.TransientModel):
	_name = "sale.order.excel.sku"

	start_date = fields.Date(string='Start Date', required=True, default=datetime.today().replace(day=1))
	end_date = fields.Date(string="End Date", required=True, default=datetime.now().replace(day = calendar.monthrange(datetime.now().year, datetime.now().month)[1]))
	user_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
	all_sale = fields.Boolean("All Salesperson")
	sale_order_data = fields.Char('Name', size=256)
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
		if not self.all_sale:
			total_order = self.env['sale.order.line'].search([('order_id.confirmation_date','>=',self.start_date),('order_id.confirmation_date','<=',self.end_date),('order_id.user_id','=',self.user_id.id)])
		if self.all_sale:
			total_order = self.env['sale.order.line'].search([('order_id.confirmation_date','>=',self.start_date),('order_id.confirmation_date','<=',self.end_date)])
		for line in total_order:
			ls = any(l2['order_no'] == str(line.order_id.name) for l2 in result)
			if not ls:
				result.append({'order_no':str(line.order_id.name), 'order_name':str(line.order_id.name), 'buyer': line.order_id.partner_id.name, 'country': line.order_id.partner_id.country_id and line.order_id.partner_id.country_id.name or '', 'user_id': line.order_id.user_id and line.order_id.user_id.name or '', 'product_id': line.product_id.name, 'name': line.name, 'quantity': line.product_uom_qty, 'uom_id': line.product_uom and line.product_uom.name, 'price_unit': line.price_unit, 'subtotal': line.price_subtotal, 'total': line.order_id.amount_total, 'freight_insurnce': line.order_id.freight_charge, 'freight_only': line.order_id.freight_only, 'insurance_only': line.order_id.insurance_only, 'bank_charge': line.order_id.bank_charge, 'extra_charge': line.order_id.ext_chrgs, 'discount': line.order_id.global_disc, 'amount_total': line.order_id.full_total, 'cost_price': 0.00, 'shipping_price': 0.00})
			if ls:
				result.append({'order_no':str(line.order_id.name), 'order_name':'', 'buyer': '', 'country': '', 'user_id': '', 'product_id': line.product_id.name, 'name': line.name, 'quantity': line.product_uom_qty, 'uom_id': line.product_uom and line.product_uom.name, 'price_unit': line.price_unit, 'subtotal': line.price_subtotal, 'total': 0.00, 'freight_insurnce': 0.00, 'freight_only': 0.00, 'insurance_only': 0.00, 'bank_charge': 0.00, 'extra_charge': 0.00, 'discount': 0.00, 'amount_total': 0.00, 'cost_price': 0.00, 'shipping_price': 0.00})
		final = sorted(result, key=lambda k: k['order_no'])
	
		

		print"-------sale_order------",final
		final_value = {}
		order_lines = []
		workbook = xlwt.Workbook()
		sheet = workbook.add_sheet('PI Product Details',cell_overwrite_ok=True)
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
		sheet.write_merge(0, 2, 0, 7, 'PI PRODUCT Report', format0)
		sheet.write(3, 0, "Start Date", format1)
		sheet.write(3, 1, final_value['start_date'], format3)
		sheet.write(3, 2, "End Date", format1)
		sheet.write(3, 3, final_value['end_date'], format3)

		sheet.write(5, 0, 'SONO.', format1)
		sheet.write(5, 1, 'BUYER', format1)
		sheet.write(5, 2, 'COUNTRY', format1)
		sheet.write(5, 3, 'COORDINATOR', format1)
		sheet.write(5, 4, 'PRODUCT', format1)
		sheet.write(5, 5, 'DESCRIPTION', format6)
		sheet.write(5, 6, 'QUANTITY', format1)
		sheet.write(5, 7, 'UOM', format6)
		sheet.write(5, 8, 'UNIT S P', format6)
		sheet.write(5, 9, 'TOTAL S P', format6)
		sheet.write(5, 10, 'TAXABLE AMOUNT',format6)
		sheet.write(5, 11, 'FREIGHT & INSURANCE',format6)
		sheet.write(5, 12, 'FREIGHT ONLY',format6)
		sheet.write(5, 13, 'INSURANCE ONLY',format6)
		sheet.write(5, 14, 'BANKING & HANDLING',format6)
		sheet.write(5, 15, 'EXTRA CHARGE',format6)
		sheet.write(5, 16, 'DISCOUNT',format6)
		sheet.write(5, 17, 'TOTAL AMOUNT',format6)
		sheet.write(5, 18, 'COST PRICE',format6)
		sheet.write(5, 19, 'SHIPPING',format6)
		row = 6 
		total_qty_pcs = 0.00
		total_price_pcs = 0.00               
		for rec in final:
			sheet.write(row, 0, rec.get('order_name'), format3)
			sheet.write(row, 1, rec.get('buyer'), format3)
			sheet.write(row, 2, rec.get('country'), format3)
			sheet.write(row, 3, rec.get('user_id'), format3)
			sheet.write(row, 4, rec.get('product_id'), format4)
			sheet.write(row, 5, rec.get('name'), format4)
			sheet.write(row, 6, rec.get('quantity'), format4)
			sheet.write(row, 7, rec.get('uom_id'), format4)
			sheet.write(row, 8, rec.get('price_unit'), format4)
			sheet.write(row, 9, rec.get('subtotal'), format4)
			sheet.write(row, 10, rec.get('total'), format4)
			sheet.write(row, 11, rec.get('freight_insurnce'), format4)
			sheet.write(row, 12, rec.get('freight_only'), format4)
			sheet.write(row, 13, rec.get('insurance_only'), format4)
			sheet.write(row, 14, rec.get('bank_charge'), format4)
			sheet.write(row, 15, rec.get('extra_charge'), format4)
			sheet.write(row, 16, rec.get('discount'), format4)
			sheet.write(row, 17, rec.get('amount_total'), format4)
			sheet.write(row, 18, rec.get('cost_price'), format4)
			sheet.write(row, 19, rec.get('shipping_price'), format4)

			row += 1
			#total_qty_pcs = total_qty_pcs + rec.get('qty_total')
			#total_price_pcs = total_price_pcs + rec.get('price_pcs')
		row += 2
		filename = ('PI Product Report'+ '.xls')
		workbook.save('/home/odoo/workspace/odoo10/odoo10/'+filename)
		file = open('/home/odoo/workspace/odoo10/odoo10/'+filename, "rb")
		file_data = file.read()
		out = base64.encodestring(file_data)
		self.write({'state': 'get', 'file_name': out, 'sale_order_data':'PI Product Report.xls'})
		return {
			'type': 'ir.actions.act_window',
			'res_model': 'sale.order.excel.sku',
			'view_mode': 'form',
			'view_type': 'form',
			'res_id': self.id,
			'target': 'new',
		}          
