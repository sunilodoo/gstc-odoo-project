# -*- coding: utf-8 -*-
from odoo import models, fields, osv, api, _
from odoo.tools.translate import _

class ResPartner(models.Model):
	_inherit = 'res.partner'
	# #-------------------------------------------------
	# visitor_no = fields.Char(string='Visitor No.')
	# visit_date = fields.Date(string='Visit Date')
	# #-------------------------------------------------

	sales_line = fields.One2many('sale.history','his_id', string='Sales History')
	classification = fields.Many2many('customer.classify', string="Classification")
	classification_id = fields.Many2one('customer.classify', string="Classification")
	company_profile = fields.Many2many('company.profile', string="Company Profile")
	product_interest = fields.Many2many('product.interest', string="Product of Interest")
	customer_code = fields.Char(compute='get_code', string='Customer Code', store=True)
	whatsapp = fields.Char(string='WhatsApp')
	wechat = fields.Char(string='WeChat')
	date_birth = fields.Date(string='DOB')
	date_aniversary = fields.Date(string='DOA')
	religion_id = fields.Many2many('customer.religion', string='Religion')
	user_id = fields.Many2one('res.users', string='Salesperson', index=True, track_visibility='onchange', default=lambda self: self.env.user)
	competitive_analysis_line = fields.One2many('competitive.analysis','compe_id', string='Competitive Analysis')

	@api.multi
	@api.depends('country_id','country_id.code','ref')
	def get_code(self):
		for res in self:
			print"-----customer_code-------",res,res.ref,res.country_id.code
			if res.ref and res.country_id and res.country_id.code:
				res.customer_code = str(res.country_id.code)+'-'+str(res.ref)

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

class CustomerClassify(models.Model):
	_name = 'customer.classify'
	name = fields.Char(string='Name', required=True)
	# _description = "Customer Classify"
	# _rec = 'customer_type'
	# _order = "customer_type asc"

	# priority_no = fields.Integer(string='Priority')
	# customer_type = fields.Char(string='Customer Type', compute='_methods_compute', store=True)
	# @api.multi
	# @api.depends('name', 'priority_no')
	# def _methods_compute(self):
	# 	for rec in self:
	# 		ct = rec.name+str(rec.priority_no).zfill(2)
	# 		rec.update({'customer_type': ct})

	name = fields.Char(string='Name')

class CompanyProfile(models.Model):
	_name = 'company.profile'

	name = fields.Char(string='Name')

class ProductInterest(models.Model):
	_name = 'product.interest'

	name = fields.Char(string='Name')

class CustomerReligion(models.Model):
	_name = 'customer.religion'

	name = fields.Char(string='Name')

class CompetitiveAnalysis(models.Model):
	_name = 'competitive.analysis'

	compe_id = fields.Many2one('res.partner', string='ID')
	name = fields.Text(string='Remarks')
	image = fields.Binary('Image')