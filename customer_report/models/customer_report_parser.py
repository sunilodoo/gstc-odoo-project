# -*- coding: utf-8 -*-
###################################################################################

from odoo.http import request
from odoo import models, api


class CustomerReportParser(models.AbstractModel):
	_name = 'report.customer_report.customer_report_template'

	@api.model
	def render_html(self, docids, data=None):
		model = self.env['res.partner'].search([('id', 'in', docids)])
		print"------------docids------",docids,model
		for i in model:
			docargs = {
				'doc': model,
			}
			return self.env['report'].render('customer_report.customer_report_template', docargs)

