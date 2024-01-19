# -*- coding: utf-8 -*-
from odoo import models, fields, osv, api, _
from odoo.tools.translate import _
from odoo.exceptions import Warning
import datetime

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
	month_unit = fields.Float('Sales/Month', compute='calc_all', track_visibility='always')
	pipeline = fields.Float(' Pipeline/ P.I Raised')
	remarks = fields.Text('Remarks')
	edd = fields.Date('Expected Date Dispatch')
	oedd = fields.Date('Orig. Expected Date Dispatch')
	target_byday = fields.Float('Target/day', compute='calc_all', track_visibility='always')
	execute_byday = fields.Float('Executed/day', compute='calc_all', track_visibility='always')
	acheive = fields.Float('Acheived (%)', compute='calc_all', track_visibility='always')

	@api.onchange('buyer')
	def change_country(self):
		print"--------------======-------",self.buyer
		if not (self.buyer and self.buyer.country_id):
			raise Warning(_("Buyer's country not defined! "))
		if self.buyer and self.buyer.country_id:
			self.country = self.buyer.country_id.id

	@api.depends('target','execute')
	def calc_all(self):
		target_byday = 0.0
		execute_byday = 0.0
		ach_per = 0.0
		month_unit = 0.0
		dic = {'apr':1, 'may':2, 'jun':3, 'jul':4, 'aug':5, 'sept':6, 'oct':7, 'nov':8, 'dec':9, 'jan':10, 'feb':11, 'mar':12}
		fin_day = datetime.date(2017, 04, 01)
		today = datetime.date.today()
		diff = today - fin_day
		for rec in self:
			if rec.target > 0 and rec.execute > 0 :
				ach_per = (rec.execute * 100)/rec.target
				rec.acheive = ach_per
			if rec.target > 0 :
				target_byday = rec.target / 365
				rec.target_byday = target_byday
			if rec.execute > 0 :
				execute_byday = rec.execute / diff.days
				rec.execute_byday = execute_byday
			if rec.month and rec.execute :
				month_unit = rec.execute / dic[rec.month]
				rec.month_unit = month_unit
			
			print"--------------======-------",rec.target,rec.target_byday,rec.month

class ResRegion(models.Model):
	_name = 'res.region'
	
	name = fields.Char(string='Name')

class finYear(models.Model):
	_name = 'fin.year'
	
	name = fields.Char(string='Name')
