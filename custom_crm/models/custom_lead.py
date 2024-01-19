# -*- coding: utf-8 -*-
from odoo import models, fields, osv, api, _
from odoo.tools.translate import _
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.exceptions import Warning
from datetime import timedelta
import datetime

class CustomLead(models.Model):
	_name = 'custom.lead'
	_description = "Custom Lead"

	name = fields.Char(string='Lead')

class CrmLead(models.Model):
	_inherit = 'crm.lead'

	visitor_no = fields.Char(related='partner_id.visitor_no', string="Visitor No", store=True)
	visit_date = fields.Date(related='partner_id.visit_date', string="Visitor Date", store=True)
	classification_id = fields.Many2one(related='partner_id.classification_id', string="Classification & Priority", store=True)
	target_value = fields.Many2one(related='partner_id.target_value', string="Target Value", store=True)
	reason_for_n_closure = fields.Many2one('closure.reason', string="Reason For Non Closure")
	tagging_custom = fields.Char(string='Tags', compute='_get_tags', store=True)
	lead = fields.Many2one('custom.lead', string="Lead", store=True)
	@api.model
	@api.onchange('tagging')
	# @api.depends('tagging')
	@api.depends('partner_id.category_id')
	def _get_tags(self):
		for rec in self:
			if rec.tagging:
				tag_custom = ','.join([p.name for p in rec.tagging])
			else:
				tag_custom = ''
			rec.tagging_custom = tag_custom