# -*- coding: utf-8 -*-
import xlwt
import base64
import logging
import calendar
from io import StringIO
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
from datetime import datetime

_logger = logging.getLogger(__name__)

class LoginUserReport(models.TransientModel):
	_name = "login.user.report"
	_description = "Login User Report"

	start_date = fields.Date(string='From Date', required=True)
	end_date = fields.Date(string="To Date", required=True)
	login_user = fields.Many2one('res.users', string='Login User')
	executed_data = fields.Char('Name', size=256)
	file_name = fields.Binary('Login User Report', readonly=True)
	state = fields.Selection([('choose', 'choose'), ('get', 'get')],
                             default='choose')



	_sql_constraints = [
		('check','CHECK((start_date <= end_date))',"To date must be greater then From date")  
	]

	def get_login_user_report(self):
		current_day = datetime.today().day
		user_record = self.env['ir.sessions'].search([('user_id','=',self.login_user.id),('date_login','>=',self.start_date),('date_logout','<=',self.end_date)])
		print("user_record:::::::::::::::::::::::::",user_record)

		# if not user_record:
		# 	_logger.info("no record found %s")

		# user_record = self.env['res.users'].search([('user_id.date_login','>=',self.start_date),('user_id.date_logout','<=',self.end_date)], order='id asc')
		# print("user_record:::::::::::::::::::::::::",user_record)
		workbook = xlwt.Workbook()
		sheet = workbook.add_sheet('Login User Details',cell_overwrite_ok=True)
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
		# sheet.col(4).width = int(30*260)   
		# sheet.col(5).width = int(50*260)
		# sheet.col(6).width = int(10*260)   
		# sheet.col(7).width = int(10*260)   
		# sheet.col(8).width = int(10*260)   
		# sheet.col(9).width = int(15*260)
		# sheet.col(10).width = int(15*260) 


		# sheet.write_merge(0, 2, 0, 10, 'Executed Sale Products Report', format0)
		# sheet.write(3, 0, "From Date", format1)
		# sheet.write(3, 1, self.start_date, format4)
		# sheet.write(3, 2, "To Date", format1)
		# sheet.write(3, 3, self.end_date, format4)
		sheet.write(0, 0, 'User Name', format1)
		sheet.write(0, 1, 'Login Date', format1)
		sheet.write(0, 2, 'Logout Date', format1)
		# sheet.write(5, 3, 'Dispatch Date', format1)
		# sheet.write(5, 4, 'Customer', format1)
		# sheet.write(5, 5, 'Products', format1)
		# sheet.write(5, 6, 'Quantity', format1)
		# sheet.write(5, 7, 'UOM', format1)
		# sheet.write(5, 8, 'Unit Price', format1)
		# sheet.write(5, 9, 'Amount Subtotal', format1)
		# sheet.write(5, 10, 'Country', format1)

		row = 1
		for line in user_record:

			# user1_record = self.env['res.users'].search([('user_id.date_login','>=',self.start_date),('user_id.date_logout','<=',self.end_date)], order='id asc')


			# sheet.write(row, 0, line.date_order.split(' ')[0], format4)
			# sheet.write(row, 1, line.confirmation_date, format4)
			# sheet.write(row, 2, line.dil_date, format4)
			# inv_id = self.env['account.invoice'].search([('order_no','=', line.name)])
			# sheet.write(row, 3, inv_id[0].dispatched_date if inv_id else '', format4)
			# sheet.write(row, 4, line.partner_id.name, format3)
			# for s_l in line.session_ids:
				# user1_record = self.env['res.users'].search([('s_l.date_login','>=',self.start_date),('s_l.date_logout','<=',self.end_date)])
				# print("user1_record::::::::::::::::::::",user1_record)
			sheet.write(row, 0, line.user_id.name)
			print("name::::::::;;;;;;;;;;;;;;;;",line.user_id.name)
			sheet.write(row, 1, line.date_login)
			print("date_login.........................",line.date_login)
			sheet.write(row, 2, line.date_logout)
			# sheet.write(row, 8, s_l.price_unit, format4)
			# sheet.write(row, 9, s_l.price_subtotal, format4)
			# sheet.write(row, 10, line.partner_country_id.name, format4)
			row += 1
	
		filename = ('Login User Report'+ '.xls')
		workbook.save('/home/odoo/workspace/odoo10/odoo10/'+filename)
		file = open('/home/odoo/workspace/odoo10/odoo10/'+filename, "rb")
		#workbook.save(filename)
		#file = open(filename, "rb")
		file_data = file.read()
		out = base64.encodestring(file_data)
		self.write({'state': 'get', 'file_name': out, 'executed_data':'Login User Report.xls'})
		return {
			'type': 'ir.actions.act_window',
			'res_model': 'login.user.report',
			'view_mode': 'form',
			'view_type': 'form',
			'res_id': self.id,
			'target': 'new',
		}          
