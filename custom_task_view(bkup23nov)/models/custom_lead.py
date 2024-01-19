# -*- coding: utf-8 -*-
from odoo import models, fields, osv, api, _
from odoo.tools.translate import _
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.exceptions import Warning
from datetime import timedelta
import datetime

class CrmLead(models.Model):
	_inherit = 'crm.lead'

	cust_type = fields.Many2one('customer.type', string="Customer Type")
	lead_image = fields.One2many('lead.image','l_id',string="Image")
	remarks = fields.Text('Remarks')

class CustomerType(models.Model):
	_name = 'customer.type'

	name = fields.Char('Name')

class LeadImage(models.Model):
	_name = 'lead.image'

	name = fields.Char('Name')
	image = fields.Binary('Image')
	l_id = fields.Many2one('crm.lead', string='Img ID')
