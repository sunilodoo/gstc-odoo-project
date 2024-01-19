# -*- coding: utf-8 -*-
from odoo import api, models
from collections import defaultdict

class CustomReports(models.AbstractModel):
	_name = 'report.custom_reports.packing_list'

	def get_order(self, object, level=0):
		so = self.env['sale.order'].search([('name','=',object.origin)])
		result = []
		result.append({'order_no':so.name, 'order_date': so.confirmation_date, 'mode_of_ship': so.carrier_id.name, 'natur_payment': so.payment_term_id.name, 'delivery_term': so.incoterms.name, 'charg_info': so.chrgs_inf})
		print"---------result----=====----result---",result
		return result

	def get_lines(self, object, level=0):
		result = []
		for line in object.packing_line_ids:
			if line.carton_no:
				carton_det = line.carton_no.split('-')
				carton_det1 = carton_det[0].zfill(4)+'-'+carton_det[1].zfill(4)
				ls = any(l2['carton_no'] == str(line.carton_no) for l2 in result)
				if not ls:
					result.append({'sr_crton':str(carton_det1), 'carton_no':str(line.carton_no), 'gross_wt': line.gross_wt, 'net_wt': line.net_wt, 'measurement': line.measurement, 'crtns': line.crtns, 'name': line.name, 'quantity': line.quantity, 'uom_id': line.uom_id and line.uom_id.name, 'remarks': line.remarks})
				if ls:
					result.append({'sr_crton':str(carton_det1), 'carton_no':'', 'gross_wt': '', 'net_wt': '', 'measurement': '', 'crtns': '', 'name': line.name, 'quantity': line.quantity, 'uom_id': line.uom_id and line.uom_id.name, 'remarks': line.remarks})
		newlist = sorted(result, key=lambda k: k['sr_crton'])
		return newlist

	def get_qty(self, object, level=0):
		result = []
		c = defaultdict(int)
		print"---------self--------",self,object
		for inv in object:
			for line in inv.packing_line_ids:
				if line.uom_id:
					print"---------line.uom_id.name===",line.uom_id.name
					result.append({'name':line.uom_id.name, 'value': line.quantity})
		print"---------result----=====----get_qty---",result
		for d in result:
			c[d['name']] += d['value']
		return [{'name': name, 'value': val} for name, val in c.items()]

	@api.multi
	def render_html(self, docids, data=None):
		print"----------report-------ppppp---",docids
		docargs = {
			'doc_ids': docids,
			'doc_model': 'packing.list',
			'docs': self.env['packing.list'].browse(docids),
			'get_order': self.get_order,
			'get_lines': self.get_lines,
			'get_qty': self.get_qty,
			'data': data,
		}
		return self.env['report'].render('custom_reports.packing_list', docargs)

class CustomReports1(models.AbstractModel):
	_name = 'report.custom_reports.commercial_invoice'

	def get_order(self, object, level=0):
		so = self.env['sale.order'].search([('name','=',object.origin)])
		result = []
		result.append({'order_no':so.name, 'order_date': so.confirmation_date, 'mode_of_ship': so.carrier_id.name, 'natur_payment': so.payment_term_id.name, 'delivery_term': so.incoterms.name, 'charg_info': so.chrgs_inf})
		print"---------result----=====----result---",result
		return result

	def get_qty(self, object, level=0):
		result = []
		c = defaultdict(int)
		print"---------self--------",self,object
		for inv in object:
			for line in inv.invoice_line_ids:
				if line.uom_id:
					print"---------line.uom_id.name===",line.uom_id.name
					result.append({'name':line.uom_id.name, 'value': line.quantity})
		print"---------result----=====----get_qty---",result
		for d in result:
			c[d['name']] += d['value']
		return [{'name': name, 'value': val} for name, val in c.items()]

	@api.multi
	def render_html(self, docids, data=None):
		print"----------report-------ppppp---",docids
		docargs = {
			'doc_ids': docids,
			'doc_model': 'account.invoice',
			'docs': self.env['account.invoice'].browse(docids),
			'get_order': self.get_order,
			'get_qty': self.get_qty,
			'data': data,
		}
		return self.env['report'].render('custom_reports.commercial_invoice', docargs)

class CustomReports2(models.AbstractModel):
	_name = 'report.custom_reports.export_invoice'
	'''	
	def get_order(self, object, level=0):
		so = self.env['sale.order'].search([('name','=',object.origin)])
		result = []
		result.append({'order_no':so.name, 'order_date': so.confirmation_date, 'mode_of_ship': so.carrier_id.name, 'natur_payment': so.payment_term_id.name, 'delivery_term': so.incoterms.name})
		print"---------result----=====----result---",result
		return result
	'''
	@api.multi
	def render_html(self, docids, data=None):
		print"----------report-------ppppp---",docids
		docargs = {
			'doc_ids': docids,
			'doc_model': 'export.invoice',
			'docs': self.env['export.invoice'].browse(docids),
			#'get_order': self.get_order,
			'data': data,
		}
		return self.env['report'].render('custom_reports.export_invoice', docargs)




