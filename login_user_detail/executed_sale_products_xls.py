# -*- coding: utf-8 -*-
import xlwt
import base64
import calendar
from io import StringIO
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
from datetime import datetime

class ExecutedSaleProductXLS(models.TransientModel):
	_name = "executed.sale.product.excel"
	_description = "Executed Sale Product XLS"

	start_date = fields.Date(string='From Date', required=True, default=datetime.today().replace(day=1))
	end_date = fields.Date(string="To Date", required=True, default=datetime.now().replace(day = calendar.monthrange(datetime.now().year, datetime.now().month)[1]))
	executed_data = fields.Char('Name', size=256)
	file_name = fields.Binary('Product Report', readonly=True)
	state = fields.Selection([('choose', 'choose'), ('get', 'get')],
                             default='choose')

	_sql_constraints = [
		('check','CHECK((start_date <= end_date))',"To date must be greater then From date")  
	]

	def get_pro_sale(self):
		current_day = datetime.today().day
		total_order = self.env['sale.order'].search([('confirmation_date','>=',self.start_date),('confirmation_date','<=',self.end_date),('state','=', 'dispatched')], order='id asc')
		workbook = xlwt.Workbook()
		sheet = workbook.add_sheet('Executed Sale Details',cell_overwrite_ok=True)
		format0 = xlwt.easyxf('font:height 500,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center')
		format1 = xlwt.easyxf('font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz center')
		# format1 = xlwt.easyxf('font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz left')
		format2 = xlwt.easyxf('font:bold True;align: horiz left')
		format3 = xlwt.easyxf('align: horiz left')
		format4 = xlwt.easyxf('align: horiz right')
		format5 = xlwt.easyxf('font:bold True;align: horiz right')
		format6 = xlwt.easyxf('font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz right')
		format7 = xlwt.easyxf('font:bold True;borders:top thick;align: horiz right')
		format8 = xlwt.easyxf('font:bold True;borders:top thick;pattern: pattern solid, fore_colour gray25;align: horiz left')
		sheet.col(0).width = int(18*260)
		sheet.col(1).width = int(18*260)    
		sheet.col(2).width = int(18*260)    
		sheet.col(3).width = int(18*260) 
		sheet.col(4).width = int(30*260)   
		sheet.col(5).width = int(50*260)
		sheet.col(6).width = int(10*260)   
		sheet.col(7).width = int(10*260)   
		sheet.col(8).width = int(10*260)   
		sheet.col(9).width = int(15*260)
		sheet.col(10).width = int(15*260) 
 

		sheet.write_merge(0, 2, 0, 10, 'Executed Sale Products Report', format0)
		sheet.write(3, 0, "From Date", format1)
		sheet.write(3, 1, self.start_date, format4)
		sheet.write(3, 2, "To Date", format1)
		sheet.write(3, 3, self.end_date, format4)
		sheet.write(5, 0, 'Order Date', format1)
		sheet.write(5, 1, 'Order Confirm Date', format1)
		sheet.write(5, 2, 'Delivery Date', format1)
		sheet.write(5, 3, 'Dispatch Date', format1)
		sheet.write(5, 4, 'Customer', format1)
		sheet.write(5, 5, 'Products', format1)
		sheet.write(5, 6, 'Quantity', format1)
		sheet.write(5, 7, 'UOM', format1)
		sheet.write(5, 8, 'Unit Price', format1)
		sheet.write(5, 9, 'Amount Subtotal', format1)
		sheet.write(5, 10, 'Country', format1)

		row = 6 
		for line in total_order:
			sheet.write(row, 0, line.date_order.split(' ')[0], format4)
			sheet.write(row, 1, line.confirmation_date, format4)
			sheet.write(row, 2, line.dil_date, format4)
			inv_id = self.env['account.invoice'].search([('order_no','=', line.name)])
			sheet.write(row, 3, inv_id[0].dispatched_date if inv_id else '', format4)
			sheet.write(row, 4, line.partner_id.name, format3)
			for s_l in line.order_line:
				sheet.write(row, 5, s_l.product_id.name, format3)
				sheet.write(row, 6, s_l.product_uom_qty, format4)
				sheet.write(row, 7, s_l.product_uom.name, format4)
				sheet.write(row, 8, s_l.price_unit, format4)
				sheet.write(row, 9, s_l.price_subtotal, format4)
				sheet.write(row, 10, line.partner_country_id.name, format4)
				row += 1
		row += 2
		filename = ('Executed Sale Products Report'+ '.xls')
		workbook.save('/usr/lib/python2.7/dist-packages/odoo/addons/'+filename)
		file = open('/usr/lib/python2.7/dist-packages/odoo/addons/'+filename, "rb")
		#workbook.save(filename)
		#file = open(filename, "rb")
		file_data = file.read()
		out = base64.encodestring(file_data)
		self.write({'state': 'get', 'file_name': out, 'executed_data':'Executed Sale Products Report.xls'})
		return {
			'type': 'ir.actions.act_window',
			'res_model': 'executed.sale.product.excel',
			'view_mode': 'form',
			'view_type': 'form',
			'res_id': self.id,
			'target': 'new',
		}          
