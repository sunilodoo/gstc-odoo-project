# -*- coding: utf-8 -*-
from odoo import models, fields, osv, api, _
from odoo.tools.translate import _
from odoo.exceptions import Warning, UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import formatLang

import odoo.addons.decimal_precision as dp


class AccountTax(models.Model):
	_inherit = 'account.tax'

	@api.model
	def _fix_tax_included_price_company(self, price, prod_taxes, line_taxes, company_id):
		if company_id:
			#To keep the same behavior as in _compute_tax_id
			prod_taxes = prod_taxes.filtered(lambda tax: tax.company_id == company_id)
			line_taxes = line_taxes.filtered(lambda tax: tax.company_id == company_id)
		return self._fix_tax_included_price(price, prod_taxes, line_taxes)

class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'
	_order = "vendor_id asc"
	_order = "edrg desc"

	cartons = fields.Float('No. of Cartons')
	vol_wt = fields.Float('Volume Wt/cartons')
	cbm = fields.Float('Total CBM')
	total_nwt_crtn = fields.Float('Total Net Weight Carton') 
	total_gwt_crtn = fields.Float('Total Gross Weight Carton')
	total_vol_wt = fields.Float('Total Volume Weight')
	is_descr = fields.Boolean('Is Descr.') 
	hsn_code = fields.Many2one('hsn.tax',string='HS Code')
	purchase_id = fields.Many2one('purchase.order', string='Po No.')
	edd = fields.Char('EDD Days')
	edrg = fields.Date('EDRG')
	adrg = fields.Date('ADRG')
	vendor_id = fields.Many2one('res.partner', string='Vendor')
	remarks = fields.Text('Remarks')
	attach_ment = fields.Binary('Attachment')
	
	@api.model
	def _get_purchase_price(self, pricelist, product, product_uom, date):
		return {}

	@api.model
	def _prepare_add_missing_fields(self, values):
		""" Deduce missing required fields from the onchange """
		res = {}
		onchange_fields = ['name', 'price_unit', 'product_uom', 'tax_id']
		if values.get('order_id') and values.get('product_id') and any(f not in values for f in onchange_fields):
			line = self.new(values)
			line.product_id_change()
			for field in onchange_fields:
				if field not in values:
					res[field] = line._fields[field].convert_to_write(line[field], line)
		return res


	@api.model
	def create(self, values):
		values.update(self._prepare_add_missing_fields(values))
		prod = self.env['product.product'].search([('id','=',values['product_id'])])
		#if not prod.toal_qty_carton >= 1:
		#	raise Warning(_('There is no any Records Of these credentials!'))
		cartons = 0
		cbm = 0
		total_nwt_crtn = 0
		total_gwt_crtn = 0
		total_vol_wt = 0
		if values['product_uom_qty'] >= 1 and prod.toal_qty_carton:
			cartons = float(values['product_uom_qty'])/float(prod.toal_qty_carton)
			cbm = (float(prod.x_attr)*float(prod.y_attr)*float(prod.z_attr)*float(cartons))/1000000
			total_nwt_crtn = float(cartons) * float(prod.carton_nwt)
			total_gwt_crtn = float(cartons) * float(prod.carton_gwt)
			total_vol_wt = float(cbm)*167
		values.update({'cartons': float(cartons), 'vol_wt': prod.vol_wt, 'cbm': float(cbm), 'total_nwt_crtn': float(total_nwt_crtn), 'total_gwt_crtn': float(total_gwt_crtn), 'total_vol_wt': float(total_vol_wt)})
		print"===values=values=",values

		line = super(SaleOrderLine, self).create(values)
		if line.state == 'sale':
			line._action_procurement_create()
			msg = _("Extra line with %s ") % (line.product_id.display_name,)
			line.order_id.message_post(body=msg)

		return line

	@api.multi
	def write(self, values):
		#result = super(SaleOrderLine, self).write(values)
		lines = False
		changed_lines = False
		if 'product_uom_qty' in values:
			precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
			lines = self.filtered(
				lambda r: r.state == 'sale' and float_compare(r.product_uom_qty, values['product_uom_qty'], precision_digits=precision) == -1)
			changed_lines = self.filtered(
				lambda r: r.state == 'sale' and float_compare(r.product_uom_qty, values['product_uom_qty'], precision_digits=precision) != 0)
			if changed_lines:
				orders = self.mapped('order_id')
				for order in orders:
				    order_lines = changed_lines.filtered(lambda x: x.order_id == order)
				    msg = ""
				    if any([values['product_uom_qty'] < x.product_uom_qty for x in order_lines]):
				        msg += "<b>" + _('The ordered quantity has been decreased. Do not forget to take it into account on your invoices and delivery orders.') + '</b>'
				    msg += "<ul>"
				    for line in order_lines:
				        msg += "<li> %s:" % (line.product_id.display_name,)
				        msg += "<br/>" + _("Ordered Quantity") + ": %s -> %s <br/>" % (line.product_uom_qty, float(values['product_uom_qty']),)
				        if line.product_id.type in ('consu', 'product'):
				            msg += _("Delivered Quantity") + ": %s <br/>" % (line.qty_delivered,)
				        msg += _("Invoiced Quantity") + ": %s <br/>" % (line.qty_invoiced,)
				    msg += "</ul>"
				    order.message_post(body=msg)
		print"---------write function----------",values,self.product_id
		cartons = 0
		cbm = 0
		total_nwt_crtn = 0
		total_gwt_crtn = 0
		total_vol_wt = 0
		if 'product_uom_qty' in values and values['product_uom_qty'] >= 1 and self.product_id.toal_qty_carton:
			cartons = float(values['product_uom_qty'])/float(self.product_id.toal_qty_carton)
			cbm = (float(self.product_id.x_attr)*float(self.product_id.y_attr)*float(self.product_id.z_attr)*float(cartons))/1000000
			total_nwt_crtn = float(cartons) * float(self.product_id.carton_nwt)
			total_gwt_crtn = float(cartons) * float(self.product_id.carton_gwt)
			total_vol_wt = float(cbm)*167
		print"------===-------------=======-----",self.product_id,

		values['cartons'] = float(cartons)
		values['vol_wt'] = self.product_id.vol_wt
		values['cbm'] = float(cbm)
		values['total_nwt_crtn'] = float(total_nwt_crtn)
		values['total_gwt_crtn'] = float(total_gwt_crtn)
		values['total_vol_wt'] = float(total_vol_wt)

		result = super(SaleOrderLine, self).write(values)
		if lines:
			lines._action_procurement_create()
		return result	

	@api.multi
	@api.onchange('product_id')
	def product_id_change(self):
		if not self.product_id:
			return {'domain': {'product_uom': []}}

		vals = {}
		domain = {'product_uom': [('category_id', '=', self.product_id.uom_id.category_id.id)]}
		if not self.product_uom or (self.product_id.uom_id.id != self.product_uom.id):
			vals['product_uom'] = self.product_id.uom_id
			vals['product_uom_qty'] = 1.0

		product = self.product_id.with_context(
			lang=self.order_id.partner_id.lang,
			partner=self.order_id.partner_id.id,
			quantity=vals.get('product_uom_qty') or self.product_uom_qty,
			date=self.order_id.date_order,
			pricelist=self.order_id.pricelist_id.id,
			uom=self.product_uom.id
		)

		result = {'domain': domain}

		title = False
		message = False
		warning = {}
		if product.sale_line_warn != 'no-message':
			title = _("Warning for %s") % product.name
			message = product.sale_line_warn_msg
			warning['title'] = title
			warning['message'] = message
			result = {'warning': warning}
			if product.sale_line_warn == 'block':
				self.product_id = False
				return result

		name = product.name_get()[0][1]
		if product.description_sale:
			name += '\n' + product.description_sale
		vals['name'] = name

		self._compute_tax_id()

		if self.order_id.pricelist_id and self.order_id.partner_id:
			vals['price_unit'] = self.env['account.tax']._fix_tax_included_price_company(self._get_display_price(product), product.taxes_id, self.tax_id, self.company_id)
		
		print"------===-------------=======-----",self.product_id,self.product_id.toal_qty_carton,self.product_uom_qty,vals
		#if not self.product_id.toal_qty_carton >= 1:
		#	raise Warning(_('There is no any Records Of these credentials!'))
		cartons = 0
		cbm = 0
		total_nwt_crtn = 0
		total_gwt_crtn = 0
		total_vol_wt = 0
		if self.product_uom_qty >=1 and self.product_id.toal_qty_carton >=1:
			cartons = float(self.product_uom_qty)/float(self.product_id.toal_qty_carton)
		
			cbm = (float(self.product_id.x_attr)*float(self.product_id.y_attr)*float(self.product_id.z_attr)*float(cartons))/1000000
			total_nwt_crtn = float(cartons) * float(self.product_id.carton_nwt)
			total_gwt_crtn = float(cartons) * float(self.product_id.carton_gwt)
			total_vol_wt = float(cbm)*167
		print"------===-------------=======-----",self.product_id,vals

		vals['cartons'] = float(cartons)
		vals['vol_wt'] = self.product_id.vol_wt
		vals['cbm'] = float(cbm)
		vals['total_nwt_crtn'] = float(total_nwt_crtn)
		vals['total_gwt_crtn'] = float(total_gwt_crtn)
		vals['total_vol_wt'] = float(total_vol_wt)

		self.update(vals)

		return result

	@api.onchange('product_uom', 'product_uom_qty')
	def product_uom_change(self):
		print"-----qty------cus---------------"
		if not self.product_uom or not self.product_id:
		    self.price_unit = 0.0
		    return
		if self.order_id.pricelist_id and self.order_id.partner_id:
			product = self.product_id.with_context(
				lang=self.order_id.partner_id.lang,
				partner=self.order_id.partner_id.id,
				quantity=self.product_uom_qty,
				date=self.order_id.date_order,
				pricelist=self.order_id.pricelist_id.id,
				uom=self.product_uom.id,
				fiscal_position=self.env.context.get('fiscal_position'),
			)
			print"-----------product_uom_change------===product_uom_change-----"
			self.price_unit = self.env['account.tax']._fix_tax_included_price_company(self._get_display_price(product), product.taxes_id, self.tax_id, self.company_id)
		
		#if not self.product_id.toal_qty_carton >= 1:
		#	raise Warning(_('There is no any Records Of these credentials!'))
		cartons = 0
		cbm = 0
		total_nwt_crtn = 0
		total_gwt_crtn = 0
		total_vol_wt = 0
		if self.product_uom_qty >= 1 and self.product_id.toal_qty_carton:
			cartons = float(self.product_uom_qty)/float(self.product_id.toal_qty_carton)
			cbm = (float(self.product_id.x_attr)*float(self.product_id.y_attr)*float(self.product_id.z_attr)*float(cartons))/1000000
			total_nwt_crtn = float(cartons) * float(self.product_id.carton_nwt)
			total_gwt_crtn = float(cartons) * float(self.product_id.carton_gwt)
			total_vol_wt = float(cbm)*167

		self.cartons = float(cartons)
		self.vol_wt = self.product_id.vol_wt
		self.cbm = float(cbm)
		self.total_nwt_crtn = float(total_nwt_crtn)
		self.total_gwt_crtn = float(total_gwt_crtn)
		self.total_vol_wt = float(total_vol_wt)



