# -*- coding: utf-8 -*-
from odoo import models, fields, osv, api, _
from odoo.tools.translate import _

class MisReporting(models.Model):
	_name = 'mis.reporting'
	
	name = fields.Many2one('hr.employee', string='Coordinator')
	salary = fields.Float('Salary')
	country = fields.Many2one('res.country', 'Country')
	buyer = fields.Many2one('res.partner', string='Buyer')
	region = fields.Many2one('res.region', string='Region')
	target = fields.Float('Target')
	target_year = fields.Many2one('fin.year', string='Financial Year')
	execute = fields.Float('Executed')
	invoice = fields.Char('Invoice Number')
	production = fields.Float('Production')
	month = fields.Selection([('jan', 'January'), ('feb', 'February'), ('mar', 'March'), ('apr', 'April'), ('may', 'May'), ('jun', 'June'), ('jul', 'July'), ('aug', 'August'), ('sept', 'September'), ('oct', 'October'), ('nov', 'November'), ('dec', 'December')], string='Dispatch Month')
	month_unit = fields.Float('Sales/Month')
	pipeline = fields.Float(' Pipeline/ P.I Raised')
	remarks = fields.Text('Remarks')

	'''
	@api.multi
	def calculate_cbm(self):
		return
	'''

class ResRegion(models.Model):
	_name = 'res.region'
	
	name = fields.Char(string='Name')

class finYear(models.Model):
	_name = 'fin.year'
	
	name = fields.Char(string='Name')
