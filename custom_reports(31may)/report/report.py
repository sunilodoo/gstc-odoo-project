# -*- coding: utf-8 -*-
from odoo import api, models

class CustomReports(models.AbstractModel):
	_name = 'report.custom_reports.packing_list'

	def get_order(self, object, level=0):
		so = self.env['sale.order'].search([('name','=',object.origin)])
		result = []
		result.append({'order_no':so.name, 'order_date': so.confirmation_date, 'mode_of_ship': so.carrier_id.name, 'natur_payment': so.payment_term_id.name, 'delivery_term': so.incoterms.name})
		print"---------result----=====----result---",result
		return result

	@api.multi
	def render_html(self, docids, data=None):
		print"----------report-------ppppp---",docids
		docargs = {
			'doc_ids': docids,
			'doc_model': 'packing.list',
			'docs': self.env['packing.list'].browse(docids),
			'get_order': self.get_order,
			'data': data,
		}
		return self.env['report'].render('custom_reports.packing_list', docargs)

class CustomReports1(models.AbstractModel):
	_name = 'report.custom_reports.commercial_invoice'

	def get_order(self, object, level=0):
		so = self.env['sale.order'].search([('name','=',object.origin)])
		result = []
		result.append({'order_no':so.name, 'order_date': so.confirmation_date, 'mode_of_ship': so.carrier_id.name, 'natur_payment': so.payment_term_id.name, 'delivery_term': so.incoterms.name})
		print"---------result----=====----result---",result
		return result

	@api.multi
	def render_html(self, docids, data=None):
		print"----------report-------ppppp---",docids
		docargs = {
			'doc_ids': docids,
			'doc_model': 'account.invoice',
			'docs': self.env['account.invoice'].browse(docids),
			'get_order': self.get_order,
			'data': data,
		}
		return self.env['report'].render('custom_reports.commercial_invoice', docargs)



