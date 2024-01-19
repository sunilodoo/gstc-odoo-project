# -*- coding: utf-8 -*-
from odoo import models, fields, osv, api, _
from odoo.tools.translate import _

class ResPartner(models.Model):
	_inherit = 'res.partner'

	sales_line = fields.One2many('sale.history','his_id', string='Sales History')
	

class SaleHistory(models.Model):
	_name = 'sale.history'

	his_id = fields.Many2one('res.partner', string='ID')
	name = fields.Char(string='Invoice no.')
	image = fields.Binary('INV Image', required=True)
	pl_image = fields.Binary('PL Image')
	pi_image = fields.Binary('PI Image')
	so_image = fields.Binary('SO Image')
	amount = fields.Float('Amount')
	currency = fields.Many2one('res.currency', string='Currency')
	date = fields.Date('Invoice Date')
	finance_yr = fields.Many2one('fin.year', string='Financial Year')

