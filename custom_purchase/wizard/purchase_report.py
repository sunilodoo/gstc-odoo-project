# -*- coding: utf-8 -*-
import xlwt
import base64
import calendar
from io import StringIO
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
from datetime import datetime

class PurchaseReportsXLS(models.TransientModel):
	_name = "purchase.report.xls"
	_description = "Purchase Reports XLS"

	start_date = fields.Date(string='From Date', required=True, default=datetime.today().replace(day=1))
	end_date = fields.Date(string="To Date", required=True, default=datetime.now().replace(day = calendar.monthrange(datetime.now().year, datetime.now().month)[1]))
	p_o_data = fields.Char('Name', size=256)
	file_name = fields.Binary('Product Report', readonly=True)
	state = fields.Selection([('choose', 'choose'), ('get', 'get')],
                             default='choose')
	state_selec = fields.Selection([
        ('all', 'All'),
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
        ], string='Status')

	_sql_constraints = [
		('check','CHECK((start_date <= end_date))',"To date must be greater then From date")  
	]

	def get_purchase_report(self):
		vals = [('bill_date','>=',self.start_date),('bill_date','<=',self.end_date)]
		if self.state_selec:
			if self.state_selec == 'all':
				pass
			else:
				vals.append(('state','=', self.state_selec))
		else:
			vals.append(('state','!=', 'draft'))
		total_order = self.env['purchase.order'].search(vals, order='id asc')
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
		sheet.write_merge(0, 2, 0, 9, 'Purchase Order Reports', format0)
		sheet.write(3, 0, "From Date", format1)
		sheet.write(3, 1, datetime.strptime(self.start_date, '%Y-%m-%d').strftime("%d-%m-%Y"), format4)
		sheet.write(3, 2, "To Date", format1)
		sheet.write(3, 3, datetime.strptime(self.end_date, '%Y-%m-%d').strftime("%d-%m-%Y"), format4)
		sheet.write(5, 0, 'Bill Date', format1)
		sheet.write(5, 1, 'Purchase Bill No.', format1)
		sheet.write(5, 2, 'Bill Total Amount', format1)
		sheet.write(5, 3, 'Bill Amount Transport & ', format1)
		sheet.write(5, 4, 'Bill Amount Packing', format1)
		sheet.write(5, 5, 'Qc Cost', format1)
		sheet.write(5, 6, 'HSN Code', format1)
		sheet.write(5, 7, 'HSN %', format1)
		sheet.write(5, 8, 'GST Amount', format1)
		sheet.write(5, 9, 'GST No. of Supplier', format1)
		sheet.write(5, 10, 'Supplier Name', format1)
		sheet.write(5, 11, 'PO No.', format1)
		sheet.write(5, 12, 'PO Date.', format1)
		sheet.write(5, 13, 'SO No.', format1)
		sheet.write(5, 14, 'SO Date.', format1)
		sheet.write(5, 15, 'SO Item Nmae', format1)
		sheet.write(5, 16, 'SO Qty', format1)
		sheet.write(5, 17, 'Status', format1)
		row = 6 
		for line in total_order:
			sheet.write(row, 0, datetime.strptime(line.bill_date, '%Y-%m-%d').strftime("%d-%m-%Y"), format3)
			sheet.write(row, 1, line.bill_no, format3)
			sheet.write(row, 2, line.amount_total, format4)
			sheet.write(row, 3, '', format4)
			sheet.write(row, 4, '', format3)
			sheet.write(row, 5, '', format3)
			sheet.write(row, 9, line.partner_id.gstn if line.partner_id.gstn else '', format3)
			sheet.write(row, 10, line.partner_id.name, format3)
			sheet.write(row, 11, line.name, format3)
			sheet.write(row, 12, datetime.strptime(line.date_order, '%Y-%m-%d %H:%M:%S').strftime("%d-%m-%Y"), format3)
			sheet.write(row, 13, line.origin, format3)
			sheet.write(row, 17, line.state, format3)
			so_name = ''
			so_id = ''
			if line.origin:
				so_name = line.origin.split(':')[0]
				so_id = self.env['sale.order'].search([('name','=', so_name)])
			sheet.write(row, 14, datetime.strptime(so_id.confirmation_date, '%Y-%m-%d').strftime("%d-%m-%Y") if so_id and so_id.confirmation_date else '', format3)
			for s_l in line.order_line:
				sheet.write(row, 6, s_l.hsn_code[0].name if s_l.hsn_code else '', format3)
				sheet.write(row, 7, s_l.taxes_id[0].name if s_l.taxes_id else '', format3)
				sheet.write(row, 8, s_l.taxes_id[0].amount if s_l.taxes_id else '', format4)
				sheet.write(row, 15, s_l.name, format3)
				sheet.write(row, 16, s_l.product_qty, format3)
				row += 1
		row += 2
		filename = ('Purchase OrderReport'+ '.xls')
		workbook.save('/home/odoo/workspace/odoo10/odoo10/'+filename)
		file = open('/home/odoo/workspace/odoo10/odoo10/'+filename, "rb")
		#workbook.save(filename)
		#file = open(filename, "rb")
		file_data = file.read()
		out = base64.encodestring(file_data)
		# self.write({'file_name': out, 'p_o_data':'Purchase Order Report.xls'})
		self.write({'state': 'get', 'file_name': out, 'p_o_data':'Purchase Order Report.xls'})
		return {
			'type': 'ir.actions.act_window',
			'res_model': 'purchase.report.xls',
			'view_mode': 'form',
			'view_type': 'form',
			'res_id': self.id,
			'target': 'new',
		}
	def get_purchase_amount(self):
		vals = [('bill_date','>=',self.start_date),('bill_date','<=',self.end_date)]
		if self.state_selec:
			if self.state_selec == 'all':
				pass
			else:
				vals.append(('state','=', self.state_selec))
		else:
			vals.append(('state','!=', 'draft'))
		total_order = self.env['purchase.order'].search(vals, order='id asc')
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
		sheet.write_merge(0, 2, 0, 9, 'Purchase Order Reports', format0)
		sheet.write(3, 0, "From Date", format1)
		sheet.write(3, 1, datetime.strptime(self.start_date, '%Y-%m-%d').strftime("%d-%m-%Y"), format4)
		sheet.write(3, 2, "To Date", format1)
		sheet.write(3, 3, datetime.strptime(self.end_date, '%Y-%m-%d').strftime("%d-%m-%Y"), format4)
		sheet.write(5, 0, 'Bill Date', format1)
		sheet.write(5, 1, 'Purchase Bill No.', format1)
		sheet.write(5, 2, 'Bill Total Amount', format1)
		sheet.write(5, 3, 'Bill Amount Transport & ', format1)
		sheet.write(5, 4, 'Bill Amount Packing', format1)
		sheet.write(5, 5, 'Qc Cost', format1)
		# sheet.write(5, 6, 'HSN Code', format1)
		# sheet.write(5, 7, 'HSN %', format1)
		# sheet.write(5, 8, 'GST Amount', format1)
		sheet.write(5, 6, 'GST No. of Supplier', format1)
		sheet.write(5, 7, 'Supplier Name', format1)
		sheet.write(5, 8, 'PO No.', format1)
		sheet.write(5, 9, 'PO Date.', format1)
		sheet.write(5, 10, 'SO No.', format1)
		sheet.write(5, 11, 'SO Date.', format1)
		# sheet.write(5, 15, 'SO Item Nmae', format1)
		# sheet.write(5, 16, 'SO Qty', format1)
		sheet.write(5, 12, 'Status', format1)
		row = 6 
		for line in total_order:
			sheet.write(row, 0, datetime.strptime(line.bill_date, '%Y-%m-%d').strftime("%d-%m-%Y"), format3)
			sheet.write(row, 1, line.bill_no, format3)
			sheet.write(row, 2, line.amount_total, format4)
			sheet.write(row, 3, '', format4)
			sheet.write(row, 4, '', format3)
			sheet.write(row, 5, '', format3)
			sheet.write(row, 6, line.partner_id.gstn if line.partner_id.gstn else '', format3)
			sheet.write(row, 7, line.partner_id.name, format3)
			sheet.write(row, 8, line.name, format3)
			sheet.write(row, 9, datetime.strptime(line.date_order, '%Y-%m-%d %H:%M:%S').strftime("%d-%m-%Y"), format3)
			sheet.write(row, 10, line.origin, format3)
			so_name = ''
			so_id = ''
			if line.origin:
				so_name = line.origin.split(':')[0]
				so_id = self.env['sale.order'].search([('name','=', so_name)])
			sheet.write(row, 11, datetime.strptime(so_id.confirmation_date, '%Y-%m-%d').strftime("%d-%m-%Y") if so_id and so_id.confirmation_date else '', format3)
			sheet.write(row, 12, line.state, format3)
			# for s_l in line.order_line:
			# 	sheet.write(row, 6, s_l.hsn_code[0].name if s_l.hsn_code else '', format3)
			# 	sheet.write(row, 7, s_l.taxes_id[0].name if s_l.taxes_id else '', format3)
			# 	sheet.write(row, 8, s_l.taxes_id[0].amount if s_l.taxes_id else '', format4)
			# 	sheet.write(row, 15, s_l.name, format3)
			# 	sheet.write(row, 16, s_l.product_qty, format3)
			row += 1
		row += 2
		filename = ('Purchase OrderReport'+ '.xls')
		workbook.save('/home/odoo/workspace/odoo10/odoo10'+filename)
		file = open('/home/odoo/workspace/odoo10/odoo10'+filename, "rb")
		#workbook.save(filename)
		#file = open(filename, "rb")
		file_data = file.read()
		out = base64.encodestring(file_data)
		# self.write({'file_name': out, 'p_o_data':'Purchase Order Report.xls'})
		self.write({'state': 'get', 'file_name': out, 'p_o_data':'Purchase Order Report.xls'})
		return {
			'type': 'ir.actions.act_window',
			'res_model': 'purchase.report.xls',
			'view_mode': 'form',
			'view_type': 'form',
			'res_id': self.id,
			'target': 'new',
		}  

                  
