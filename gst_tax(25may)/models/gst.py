# -*- coding: utf-8 -*-

from openerp import models, fields, osv, api, _
from openerp.tools.translate import _
import re

class product_product(models.Model):
	_inherit = 'product.product'
	
	hsn_code = fields.Many2one('hsn.tax',string='HS Code')
	
class hsn_tax(models.Model):
	_name = 'hsn.tax'
	
	name = fields.Char(string='HS Code', required=True)
	cgst = fields.Many2one('account.tax', string='CGST', domain="[('name', 'like', 'CGST')]")
	sgst = fields.Many2one('account.tax', string='SGST', domain="[('name', 'like', 'SGST')]")
	igst = fields.Many2one('account.tax', string='IGST', domain="[('name', 'like', 'GST')]")

	_sql_constraints = [
        ('name_company_uniq', 'unique(name)', 'The name of the HSN must be unique!'),
    ]

class ResPartner(models.Model):
	_inherit = 'res.partner'

	gstn = fields.Char('GSTIN No.')
	old_customer = fields.Boolean('Old/Lost Customer')
	compt_customer = fields.Boolean('competitor Customer')
	new_customer = fields.Boolean('New Customer')
	trgt = fields.Float('Target')
	potvl = fields.Char('Potential value')

class ResCompany(models.Model):
	_inherit = 'res.company'

	gstn = fields.Char('GSTIN No.')
	iso_no = fields.Char('ISO No.')
	rev_no = fields.Char('Revision No.')

class purchase_order_line(models.Model):
	_inherit = 'purchase.order.line'

	hsn_code = fields.Many2one('hsn.tax',string='HS Code')
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


