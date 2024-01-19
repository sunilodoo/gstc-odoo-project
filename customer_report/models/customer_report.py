# -*- coding: utf-8 -*-
###################################################################################
from odoo import models, fields, api, _
import xlwt
import xlwt
import base64
import calendar
from io import StringIO
from datetime import datetime

class CustomerReportButton(models.TransientModel):
	_name = 'wizard.customer.report'

	preferences = fields.Selection([('customer','customer'),('vendor','vendor'),('both','both')], string="Preference", required=True)
	sale_order_data = fields.Char('Name', size=256)
	file_name = fields.Binary('Customer Report', readonly=True)
	state = fields.Selection([('choose', 'choose'), ('get', 'get')],
		         default='choose')

	@api.multi
	def print_customer_report_pdf(self):
		print"-----------customer-------",self,self.preferences
		if self.preferences and self.preferences == 'customer':
			record = self.env['res.partner'].search([('customer','=', True)])
		if self.preferences and self.preferences == 'vendor':
			record = self.env['res.partner'].search([('supplier','=', True)])
		if self.preferences and self.preferences == 'both':
			record = self.env['res.partner'].search([])
		return self.env['report'].get_action(record, "customer_report.customer_report_template")

	@api.multi
	def print_customer_report_xls(self):
		final = []
		final2 = []
		final4 = []
		current_day = datetime.today().day
		print"-----------ddfdsfjdsj----dkfdk======",current_day,self,self.preferences
		if self.preferences and self.preferences == 'customer':
			record = self.env['res.partner'].search([('customer','=', True)])
		if self.preferences and self.preferences == 'vendor':
			record = self.env['res.partner'].search([('supplier','=', True)])
		if self.preferences and self.preferences == 'both':
			record = self.env['res.partner'].search([])
		if record:
			for l in record:
				final.append({'customer': l.name, 'address': l.street, 'country': l.country_id.name, 'salesperson': l.user_id.name, 'classification': l.classification_id.name, 'profile': ', '.join(map(lambda x: x.name, l.company_profile)), 'poi': ', '.join(map(lambda x: x.name, l.product_interest)), 'tags': ', '.join(map(lambda x: x.name, l.category_id)), 'email': l.email, 'phone': l.phone, 'mobile': l.mobile, 'whatsapp': l.whatsapp, 'wechat': l.wechat, 'dob': l.date_birth, 'doa': l.date_aniversary, 'religion': l.name, 'create_dates': str(l.create_date)})



		sale_order = self.env.cr.fetchall()      
		print"-------sale_order------",final
		final_value = {}
		order_lines = []
		workbook = xlwt.Workbook()
		sheet = workbook.add_sheet('Customer Details',cell_overwrite_ok=True)
		final_value['start_date'] = self.preferences
		final_value['end_date'] = self.preferences
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
		sheet.write_merge(0, 2, 0, 7, 'CUSTOMER DETAILS REPORT' , format0)
		#sheet.write(3, 0, "Start Date", format1)
		#sheet.write(3, 1, final_value['start_date'], format3)
		#sheet.write(3, 2, "End Date", format1)
		#sheet.write(3, 3, final_value['end_date'], format3)

		sheet.write(5, 0, 'Company Name', format1)
		sheet.write(5, 1, 'Address', format1)
		sheet.write(5, 2, 'Country', format1)
		sheet.write(5, 3, 'Salesperson', format1)
		sheet.write(5, 4, 'Classification', format1)
		sheet.write(5, 5, 'Company Profile', format1)
		sheet.write(5, 6, 'Product of Interest', format1)
		sheet.write(5, 7, 'Tags', format1)
		sheet.write(5, 8, 'Email', format1)
		sheet.write(5, 9, 'Phone', format1)
		sheet.write(5, 10, 'Mobile', format1)
		sheet.write(5, 11, 'WhatsApp', format1)
		sheet.write(5, 12, 'WeChat', format1)
		sheet.write(5, 13, 'DOB', format1)
		sheet.write(5, 14, 'DOA', format1)
		sheet.write(5, 15, 'Religion', format1)
		sheet.write(5, 16, 'Create Date', format1)

		row = 6 
		total_qty_pcs = 0.00
		total_price_pcs = 0.00               
		for rec in final:
			sheet.write(row, 0, rec.get('customer'), format3)
			sheet.write(row, 1, rec.get('address'), format3)
			sheet.write(row, 2, rec.get('country'), format3)
			sheet.write(row, 3, rec.get('salesperson'), format3)
			sheet.write(row, 4, rec.get('classification'), format3)
			sheet.write(row, 5, rec.get('profile'), format3)
			sheet.write(row, 6, rec.get('poi'), format3)
			sheet.write(row, 7, rec.get('tags'), format3)
			sheet.write(row, 8, rec.get('email'), format3)
			sheet.write(row, 9, rec.get('phone'), format3)
			sheet.write(row, 10, rec.get('mobile'), format3)
			sheet.write(row, 11, rec.get('whatsapp'), format3)
			sheet.write(row, 12, rec.get('wechat'), format3)
			sheet.write(row, 13, rec.get('dob'), format3)
			sheet.write(row, 14, rec.get('doa'), format3)
			sheet.write(row, 15, rec.get('religion'), format3)
			sheet.write(row, 16, rec.get('create_dates'), format3)
			#sheet.write(row, 4, rec.get('price_pcs'), format4)
			row += 1
			#total_qty_pcs = total_qty_pcs + rec.get('qty_total')
			#total_price_pcs = total_price_pcs + rec.get('price_pcs')
		row += 2
		#sheet.write(row+0, 0,'TOTAL', format8)
		#sheet.write(row+0, 3, total_qty_pcs, format8)
		#sheet.write(row+0, 4, total_price_pcs, format8)
		filename = ('/home/odoo/workspace/odoo10/odoo10/addons/customer_report/Security/Customer Report'+ '.xls')
		workbook.save(filename)
		file = open(filename, "rb")
		file_data = file.read()
		out = base64.encodestring(file_data)
		self.write({'state': 'get', 'file_name': out, 'sale_order_data':'Customer Report.xls'})
		return {
			'type': 'ir.actions.act_window',
			'res_model': 'wizard.customer.report',
			'view_mode': 'form',
			'view_type': 'form',
			'res_id': self.id,
			'target': 'new',
		} 
