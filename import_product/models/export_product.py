# -*- coding: utf-8 -*-
###################################################################################
from odoo import models, fields, api, _
import xlwt
import base64
import calendar
from io import StringIO
from datetime import datetime

class ProductExportWizard(models.TransientModel):
	_name = 'product.export'

	data = fields.Char('Name', size=256)
	file_name = fields.Binary('Product Export', readonly=True)
	state = fields.Selection([('choose', 'choose'), ('get', 'get')],
		         default='choose')

	@api.multi
	def export_product(self):
		final = []
		current_day = datetime.today().day

		final_value = {}
		order_lines = []
		workbook = xlwt.Workbook()
		sheet = workbook.add_sheet('Product Details',cell_overwrite_ok=True)
		format0 = xlwt.easyxf('font:height 500,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center')
		format1 = xlwt.easyxf('font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz left')
		format2 = xlwt.easyxf('font:bold True;align: horiz left')
		format3 = xlwt.easyxf('align: horiz left')
		format4 = xlwt.easyxf('align: horiz right')
		format5 = xlwt.easyxf('font:bold True;align: horiz right')
		format6 = xlwt.easyxf('font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz right')
		format7 = xlwt.easyxf('font:bold True;borders:top thick;align: horiz right')
		format8 = xlwt.easyxf('font:bold True;borders:top thick;pattern: pattern solid, fore_colour gray25;align: horiz left')

		sheet.col(0).width = int(15*260)
		sheet.col(1).width = int(50*260)    
		sheet.col(2).width = int(18*260)    
		sheet.col(3).width = int(18*260) 
		sheet.col(4).width = int(15*260)   
		sheet.col(5).width = int(30*260)
		sheet.col(6).width = int(33*260)     

		sheet.write(0, 0, 'Item Code', format1)
		sheet.write(0, 1, 'Product', format1)
		sheet.write(0, 2, 'UoM', format1)
		sheet.write(0, 3, 'Attribute Type', format1)
		sheet.write(0, 4, 'Attribute Value', format1)
		sheet.write(0, 5, 'Vendor', format1)
		sheet.write(0, 6, 'Primary Unit', format1)
		sheet.write(0, 7, 'Pri. Net Weight', format1)
		sheet.write(0, 8, 'Pri. Gross Weight', format1)
		sheet.write(0, 9, 'Unit in carton Qty.', format1)
		sheet.write(0, 10, 'Total Qty. in Carton', format1)
		sheet.write(0, 11, 'Carton Net Weight', format1)
		sheet.write(0, 12, 'Carton Gross Weight', format1)
		sheet.write(0, 13, 'Length', format1)
		sheet.write(0, 14, 'Width', format1)
		sheet.write(0, 15, 'Height', format1)
		sheet.write(0, 16, 'Unit carton CBM', format1)

		row = 1 
		total_qty_pcs = 0.00
		total_price_pcs = 0.00 
		product_ids = self.env['product.product'].search([('active','=',True)])
		for product in product_ids:
			sheet.write(row, 0, product.item_code or '', format3)
			sheet.write(row, 1, product.name or '', format3)
			sheet.write(row, 2, product.uom_id and product.uom_id.name or '', format3)
			sheet.write(row, 3, product.attribute_value_ids and ', '.join(x.attribute_id.name for x in product.attribute_value_ids) or '', format3)
			sheet.write(row, 4, product.attribute_value_ids and ', '.join(x.name for x in product.attribute_value_ids) or '', format3)
			sheet.write(row, 5, product.seller_ids and ', '.join(x.name.name for x in product.seller_ids) or '', format3)
			sheet.write(row, 6, product.no_of_catons and product.no_of_catons or '', format3)
			sheet.write(row, 7, product.net_weight and product.net_weight or 0, format3)
			sheet.write(row, 8, product.gross_weight and product.gross_weight or 0, format3)
			sheet.write(row, 9, product.no_of_item and product.no_of_item or 0, format3)
			sheet.write(row, 10, product.toal_qty_carton and product.toal_qty_carton or 0, format3)
			sheet.write(row, 11, product.carton_nwt and product.carton_nwt or 0, format3)
			sheet.write(row, 12, product.carton_gwt and product.carton_gwt or 0, format3)
			sheet.write(row, 13, product.x_attr and product.x_attr or 0, format3)
			sheet.write(row, 14, product.y_attr and product.y_attr or 0, format3)
			sheet.write(row, 15, product.z_attr and product.z_attr or 0, format3)
			sheet.write(row, 16, product.vol_wt and product.vol_wt or 0, format3)
			row += 1
		row += 2
		filename = ('/home/odoo/workspace/odoo10/odoo10/addons/customer_report/Security/Customer Report'+ '.xls')
		workbook.save(filename)
		file = open(filename, "rb")
		file_data = file.read()
		out = base64.encodestring(file_data)
		self.write({'state': 'get', 'file_name': out, 'data':'Product Export.xls'})
		return {
			'type': 'ir.actions.act_window',
			'res_model': 'product.export',
			'view_mode': 'form',
			'view_type': 'form',
			'res_id': self.id,
			'target': 'new',
		} 
