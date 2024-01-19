# -*- coding: utf-8 -*-
from odoo import models, fields, osv, api, _
from odoo.tools.translate import _

class ResPartner(models.Model):
	_inherit = 'res.partner'

	visitor_no = fields.Char(string='Visitor No.', copy=False)
	visit_date = fields.Date(string='Visit Date')
class InheritCustomerClassify(models.Model):
	_inherit = 'customer.classify'
	_description = "Customer Classify"

	# _rec = 'customer_type'
	# _order = "customer_type asc"

	name = fields.Char(string='Name', required=True)
	# name = fields.Char(string='Name', required=True, readonly=True)
	# name = fields.Char(string='Name', required=True, readonly=True,  default=lambda self: str(self.priority_no).zfill(2)+self.customer_type)
	priority_no = fields.Integer(string='Priority', required=True)
	customer_type = fields.Char(string='Customer Type', required=True)
	# customer_type = fields.Char(string='Customer Type', compute='_methods_compute', store=True)
	@api.multi
	# @api.depends('customer_type', 'priority_no')
	@api.onchange('name', 'customer_type', 'priority_no')
	def methods_compute(self):
		for rec in self:
			if rec.priority_no and rec.customer_type:
				ct = str(rec.priority_no).zfill(2)+'. '+rec.customer_type
				rec.update({'name': ct})

class ReasonForNonClosure(models.Model):
	_name = 'closure.reason'
	_description = "Reason For Non Closure"

	name = fields.Char(string='Reason For Non-Closure')