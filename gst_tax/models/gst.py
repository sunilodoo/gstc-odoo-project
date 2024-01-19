# -*- coding: utf-8 -*-

from openerp import models, fields, osv, api, _
from openerp.tools.translate import _
from odoo.exceptions import UserError, ValidationError
import re

class product_product(models.Model):
	_inherit = 'product.product'
	
	hsn_code = fields.Many2one('hsn.tax',string='HS Code')
	@api.onchange('hsn_code')
	def _onchange_hsn_code(self):
		if self.hsn_code:
			self.supplier_taxes_id = self.hsn_code.igst
		if not self.hsn_code:
			self.supplier_taxes_id = ''
class ProductTemplate(models.Model):
	_inherit = 'product.template'

	hsn_code = fields.Many2one('hsn.tax',string='HS Code', compute='_compute_hsn_code', inverse='_set_hsn_code')
	@api.onchange('hsn_code')
	def _onchange_hsn_code(self):
		if self.hsn_code:
			self.supplier_taxes_id = self.hsn_code.igst
		if not self.hsn_code:
			self.supplier_taxes_id = ''
	@api.depends('product_variant_ids', 'product_variant_ids.hsn_code')
	def _compute_hsn_code(self):
		unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
		for template in unique_variants:
			template.hsn_code = template.product_variant_ids.hsn_code
		for template in (self - unique_variants):
			template.hsn_code = 0.0
	@api.one
	def _set_hsn_code(self):
		if len(self.product_variant_ids) == 1:
			self.product_variant_ids.hsn_code = self.hsn_code
	
class hsn_tax(models.Model):
	_name = 'hsn.tax'
	
	name = fields.Char(string='HS Code', required=True)
	cgst = fields.Many2one('account.tax', string='CGST', domain="[('name', 'like', 'CGST')]")
	sgst = fields.Many2one('account.tax', string='SGST', domain="[('name', 'like', 'SGST')]")
	igst = fields.Many2one('account.tax', string='GST', domain="[('name', 'like', 'GST')]", required=True)

	_sql_constraints = [
        ('name_company_uniq', 'unique(name)', 'The name of the HSN must be unique!'),
    ]
	@api.constrains('name')
	def check_name_length(self):
		for rec in self:
			if len(rec.name) != 8:
				raise ValidationError(_('HS Code must be 8 Characters'))

class ResPartner(models.Model):
	_inherit = 'res.partner'

	gstn = fields.Char('GSTIN No.', default='Import By')
	partner_vat_name = fields.Char(string='Partner VAT Name')
	old_customer = fields.Boolean('Old/Lost Customer')
	compt_customer = fields.Boolean('competitor Customer')
	new_customer = fields.Boolean('New Customer')
	trgt = fields.Float('Target')
	potvl = fields.Char('Potential value')
	delay_day = fields.Integer('Delay Days', default=5)
	gstin_line_ids = fields.One2many('gstin.line', 'line_id', string="GSTIN Line")
	# gstin_line_ids = fields.One2many('gstin.line', 'order_id', string="GSTIN Line", compute='_compute_vendor_list')
	@api.constrains('gstin_line_ids', 'supplier')
	# @api.constrains('gstin_line_ids', 'country_id', 'supplier')
	def check_gstn_length(self):
		if self.supplier == True:
			# print("---------------self.supplier--------", self.supplier)
			# print("---------------asd--------", self.gstin_line_ids)
			# print("-------------2--asd--------", len(self.gstin_line_ids))
			if len(self.gstin_line_ids) == 0:
				if self.country_id.name != 'India':
					raise ValidationError(_('Vendor must have a GSTIN No. as Import By'))
				if self.country_id.name == 'India':
					raise ValidationError(_('Vendor must be a GSTIN No.'))
			if self.country_id.name != 'India':
				g_l_ids = self.gstin_line_ids
				for g_l in g_l_ids:
					if g_l.name != 'Import By':
						raise ValidationError(_('Outside India Vendor must have a GSTIN No. as Import By'))
					if g_l.site:
						raise ValidationError(_('Outside India Vendor site must be empty'))
					if g_l.state_id:
						raise ValidationError(_('Outside India Vendor State Name must be empty'))
			if self.country_id.name == 'India':
				g_l_ids = self.gstin_line_ids
				for g_l in g_l_ids:
					if not g_l.name:
						raise ValidationError(_('Vendor must be a GSTIN No.'))
					if g_l.name == 'Import By':
						raise ValidationError(_('Indian Vendor must have a valid 15 digits GSTIN No. rather than Import By '))
					if len(g_l.name) != 15:
						raise ValidationError(_('GSTIN No. must be 15 Characters'))
					if not g_l.site:
						raise ValidationError(_('Vendor GSTIN must be a site name'))
					if not g_l.state_id:
						raise ValidationError(_('Vendor GSTIN must have a state name'))
		if self.supplier != True and self.gstin_line_ids:
			raise ValidationError(_('Partner is not a Vendor, Remove GSTIN From GSTIN Line'))
		# if self.country_id.name == 'India' and self.supplier == True:
		# 	g_l_ids = self.gstin_line_ids
		# 	for g_l in g_l_ids:
		# 		if not g_l.name:
		# 			raise ValidationError(_('Vendor must be a GSTIN No.'))
		# 		if g_l.name == 'Import By':
		# 			raise ValidationError(_('Indian Vendor must have a valid 15 digits GSTIN No. rather than Import By '))
		# 		if len(g_l.name) != 15:
		# 			raise ValidationError(_('GSTIN No. must be 15 Characters'))
		# 		if not g_l.site:
		# 			raise ValidationError(_('Vendor GSTIN must be a site name'))
		# 		if not g_l.state_id:
		# 			raise ValidationError(_('Vendor GSTIN must have a state name'))
		# if self.country_id.name != 'India' and self.supplier == True:
		# 	g_l_ids = self.gstin_line_ids
		# 	for g_l in g_l_ids:
		# 		if g_l.name != 'Import By':
		# 			raise ValidationError(_('Outside India Vendor must have a GSTIN No. as Import By '))
		# 		if g_l.site:
		# 			raise ValidationError(_('Outside India Vendor site must be empty'))
		# 		if g_l.state_id:
		# 			raise ValidationError(_('Outside India Vendor State Name must be empty'))
class PartnerGstinLine(models.Model):
	_name = 'gstin.line'
	_description = 'Partner Gstin Line'
	_order = 'id'
	line_id = fields.Many2one('res.partner', string='Partner Reference', index=True, copy=False)
	# supplier = fields.Boolean(related='order_id.supplier', string='Is a Vendor',store=True)
	# order_id = fields.Many2one('res.partner', string='Partner Reference', required=True, ondelete='cascade', index=True, copy=False)
	name = fields.Char('GSTIN No.', default='Import By')
	site = fields.Char('Site.')
	# country_id = fields.Many2one('res.country', 'State Name', domain="[('country_id', '=', 105)]")
	state_id = fields.Many2one('res.country.state', 'State Name', domain="[('country_id', '=', 105)]")
	# @api.constrains('name')
	# def check_gstn_length(self):
	# 	# if self.supplier == True:
	# 	# if not self.name:
	# 	# 	raise ValidationError(_('Vendor must be a valid GSTIN No.'))
	# 	print"------------self.order_id.country_id.name-----",self.order_id.country_id.name
	# 	if self.order_id.country_id.name == 'India':
	# 		if len(self.name) != 15:
	# 			raise ValidationError(_('GSTIN No. must be 15 Characters'))
	# 	else:
	# 	# if self.order_id.country_id.name != 'India':
	# 		self.name = 'Import By'

    # @api.depends('state', 'product_uom_qty', 'qty_delivered', 'qty_to_invoice', 'qty_invoiced')
    # def _compute_invoice_status(self):
class ResCompany(models.Model):
	_inherit = 'res.company'

	gstn = fields.Char('GSTIN No.')
	iso_no = fields.Char('ISO No.')
	rev_no = fields.Char('Revision No.')
	iec_no = fields.Char('IEC No.')

class purchase_order_line(models.Model):
	_inherit = 'purchase.order.line'

	hsn_code = fields.Many2one('hsn.tax', string='HS Code')
	#remarks = fields.Text('Remarks')

	'''
	@api.onchange('hsn_code')
	def onchange_hsn_code(self):
		print"----------hsn-------code------change---",self
		hsn_tax = self.env['hsn.tax'].search([('id','=',self.hsn_code.id)])
		if hsn_tax:
			print"----------hsn-------code------change---",hsn_tax,hsn_tax.igst
			self.taxes_id = [[6,0, [hsn_tax.igst.id]]]

	'''

class res_country_state(models.Model):
	_inherit = 'res.country.state'

	govt_code = fields.Char(string='Code')


