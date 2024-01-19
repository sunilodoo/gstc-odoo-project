# -*- coding: utf-8 -*-
import xlwt
import base64
import calendar
from io import StringIO
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
from datetime import datetime

class CRMLeadExport(models.TransientModel):
	_name = "crm.lead.export"
	_description = "CRM Lead Exportt XLS"

	# start_date = fields.Date(string='From Date', required=True, default=datetime.today().replace(day=1))
	# end_date = fields.Date(string="To Date", required=True, default=datetime.now().replace(day = calendar.monthrange(datetime.now().year, datetime.now().month)[1]))
	source_id = fields.Many2one('utm.source', string='Source')
	export_data = fields.Char('Name', size=256)
	file_name = fields.Binary('CRM Lead Exportt' , readonly=True)
	state = fields.Selection([('choose', 'choose'), ('get', 'get')],
                             default='choose')

	# _sql_constraints = [
	# 	('check','CHECK((start_date <= end_date))',"To date must be greater then From date")  
	# ]

	def date_export(self):
		# current_day = datetime.today().day
		val=[]
		if self.source_id:
			val.append(('source_id', '=', self.source_id.id))
		crm_leads_ids = self.env['crm.lead'].search(val)
		# crm_leads_ids = self.env['crm.lead'].search([], order='id asc')
		workbook = xlwt.Workbook()
		sheet = workbook.add_sheet('CRM Lead Exportt', cell_overwrite_ok=True)
		format0 = xlwt.easyxf('font:height 500,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center')
		format1 = xlwt.easyxf('font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz center')
		format2 = xlwt.easyxf('font:bold True;align: horiz left')
		format3 = xlwt.easyxf('align: horiz left')
		format4 = xlwt.easyxf('align: horiz right')
		format5 = xlwt.easyxf('font:bold True;align: horiz right')
		format6 = xlwt.easyxf('font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz right')
		format7 = xlwt.easyxf('font:bold True;borders:top thick;align: horiz right')
		format8 = xlwt.easyxf('font:bold True;borders:top thick;pattern: pattern solid, fore_colour gray25;align: horiz left')
		sheet.write(0, 0, 'ID', format1)
		sheet.write(0, 1, 'Opportunity', format1)
		sheet.write(0, 2, 'Company', format1)
		sheet.write(0, 3, 'Country', format1)
		sheet.write(0, 4, 'Contact Person', format1)#Contact Name
		sheet.write(0, 5, 'Email', format1)
		sheet.write(0, 6, 'Mobile', format1)
		sheet.write(0, 7, 'Phone', format1)
		sheet.write(0, 8, 'Source', format1)
		sheet.write(0, 9, 'Medium', format1)
		sheet.write(0, 10, 'Tags', format1)
		sheet.write(0, 11, 'Leads', format1)
		sheet.write(0, 12, 'Product of Interest', format1)
		sheet.write(0, 13, 'Sales Team', format1)
		sheet.write(0, 14, 'Next Activity', format1)
		sheet.write(0, 15, 'Action Date', format1)
		sheet.write(0, 16, 'Title Action', format1)
		sheet.write(0, 17, 'Expected Closing', format1)
		sheet.write(0, 18, 'Salspersion', format1)
		sheet.write(0, 19, 'Customer Type', format1)
		sheet.write(0, 20, 'Visitor No', format1)
		sheet.write(0, 21, 'Visitor Date', format1)
		sheet.write(0, 22, 'Classification & Priority', format1)
		sheet.write(0, 23, 'Target Value', format1)
		sheet.write(0, 24, 'Rating', format1)
		sheet.write(0, 25, 'Days to Assign', format1)
		sheet.write(0, 26, 'Days to Close', format1)
		sheet.write(0, 27, 'Potential value', format1)
		sheet.write(0, 28, 'Reason for Non Closure', format1)
		sheet.write(0, 29, 'Description', format1)
		row = 1 
		for line in crm_leads_ids:
			sheet.write(row, 0, line.id, format4)
			sheet.write(row, 1, line.name, format3)
			sheet.write(row, 2, line.partner_id.name if line.partner_id else '', format3)
			sheet.write(row, 3, line.partner_id.country_id.name if line.partner_id.country_id else '', format3)
			sheet.write(row, 4, line.partner_id.child_ids[0].name if line.partner_id.child_ids else '', format3)
			sheet.write(row, 5, line.email_from if line.email_from else '', format3)
			sheet.write(row, 6, line.partner_id.mobile if line.partner_id.mobile else '', format3)
			sheet.write(row, 7, line.phone if line.phone else '', format3)
			sheet.write(row, 8, line.source_id.name if line.source_id else '', format3)
			sheet.write(row, 9, line.medium_id.name if line.medium_id else '', format3)
			sheet.write(row, 11, line.lead.name if line.lead else '', format3)
			sheet.write(row, 13, line.team_id.name if line.team_id else '', format3)
			sheet.write(row, 14, line.next_activity_id.name if line.next_activity_id else '', format3)
			sheet.write(row, 15, line.date_action if line.date_action else '', format3)
			sheet.write(row, 16, line.title_action if line.title_action else '', format3)
			sheet.write(row, 17, line.date_deadline if line.date_deadline else '', format3)
			sheet.write(row, 18, line.user_id.name if line.user_id else '', format3)
			sheet.write(row, 19, line.cust_type.name if line.cust_type else '', format3)
			sheet.write(row, 20, line.visitor_no if line.visitor_no else '', format3)
			sheet.write(row, 21, line.visit_date if line.visit_date else '', format3)
			sheet.write(row, 22, line.classification_id.name if line.classification_id else '', format3)
			sheet.write(row, 23, line.target_value.name if line.target_value else '', format3)
			sheet.write(row, 24, line.priority if line.priority else '', format4)
			sheet.write(row, 25, line.day_open if line.day_open else '', format3)
			sheet.write(row, 26, line.day_close if line.day_close else '', format3)
			sheet.write(row, 27, line.referred if line.referred else '', format3)
			sheet.write(row, 28, line.reason_for_n_closure.name if line.reason_for_n_closure else '', format3)
			sheet.write(row, 29, line.description if line.description else '', format3)
			loop_count = 0
			index = 0
			pis = [pi_line.name for pi_line in  line.product_interest]
			pis_len = len(pis)
			tags = [tag_line.name for tag_line in  line.tagging]
			tags_len = len(tags)
			if pis_len >= tags_len:
				loop_count = pis_len
			else:
				loop_count = tags_len
			for i in range(loop_count):
				sheet.write(row, 0, line.id, format4)
				if pis_len > i:
					sheet.write(row, 12, pis[i], format3)
				if tags_len > i:
					sheet.write(row, 10, tags[i], format3)
				index += 1
				row += 1
			if pis_len >= 1 or tags_len >= 1:
				row =row-1 
			# for s_l in line.order_line:
			# 	sheet.write(row, 5, s_l.product_id.name, format3)
			# 	sheet.write(row, 6, s_l.product_uom_qty, format4)
			# 	sheet.write(row, 7, s_l.product_uom.name, format4)
			# 	sheet.write(row, 8, s_l.price_unit, format4)
			# 	sheet.write(row, 9, s_l.price_subtotal, format4)
			row += 1
		# row += 2
		filename = ('CRM Lead Export'+ '.xls')
		workbook.save('/home/odoo/workspace/odoo10/odoo10/'+filename)
		file = open('/home/odoo/workspace/odoo10/odoo10/'+filename, "rb")
		#workbook.save(filename)
		#file = open(filename, "rb")
		file_data = file.read()
		out = base64.encodestring(file_data)
		self.write({'state': 'get', 'file_name': out, 'export_data':'CRM Lead Export.xls'})
		return {
			'type': 'ir.actions.act_window',
			'res_model': 'crm.lead.export',
			'view_mode': 'form',
			'view_type': 'form',
			'res_id': self.id,
			'target': 'new',
		}          
