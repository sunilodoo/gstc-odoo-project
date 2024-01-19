# -*- coding: utf-8 -*-
from odoo import models, fields, osv, api, _
from odoo.tools.translate import _

class ProductProduct(models.Model):
	_inherit = 'product.product'

	item_code = fields.Char('Item Code')
	no_of_catons = fields.Integer('Primary Unit', required=True)
	net_weight = fields.Float('Pri. Net Weight')
	gross_weight = fields.Float('Pri. Gross Weight')
	no_of_item = fields.Integer('Unit in carton Qty.', required=True)
	toal_qty_carton = fields.Integer('Total Qty. in Carton', )
	carton_nwt = fields.Float('Carton Net Weight')
	carton_gwt = fields.Float('Carton Gross Weight')
	x_attr = fields.Float('Len', required=True)
	y_attr = fields.Float('Breadth',required=True) 
	z_attr = fields.Float('Height',required=True)
	total_qty = fields.Float('Total Qty')
	cartons = fields.Float('Cartons')
	vol_wt = fields.Float('Unit carton CBM', )
	cbm = fields.Float('CBM', readonly=True)
	total_vol_wt = fields.Float('Total Volume Weight')
	total_nwt_crtn = fields.Float('Total Net Weight Carton') 
	total_gwt_crtn = fields.Float('Total Gross Weight Carton') 

	comp = fields.Char(compute="calculate_cbm", string="Calc. CBM")

	@api.multi
	def calculate_cbm(self):
		print "ENTRY=---",self
		#tmpl = self.env['product.template'].search([('id','=',self.product_tmpl_id.id)])
		#print"-----tmpl--------",tmpl.attribute_line_ids.item_code,tmpl.attribute_line_ids.no_of_catons,
		'''
		for line in self.attribute_line_ids:
			#ttl_qty_crtn = 1.0
			#cbm = 1.0
			#crtns = 1.0
			vol_per_crtn = 1.0
			#ttl_vol_wt = 1.0
			#ttl_nwt_crtn = 1.0
			#ttl_gwt_crtn = 1.0
			ttl_qty_crtn = line.no_of_catons * line.no_of_item
			#crtns = line.total_qty / ttl_qty_crtn
			vol_per_crtn = (line.x_attr * line.y_attr * line.z_attr)/1000000
			#cbm = (line.x_attr * line.y_attr * line.z_attr * crtns)/1000000
			#ttl_vol_wt = cbm * 167
			#ttl_nwt_crtn = crtns * line.carton_nwt
			#ttl_gwt_crtn = crtns * line.carton_gwt
			#line.write({'toal_qty_carton': ttl_qty_crtn, 'cbm': cbm, 'cartons': crtns, 'vol_wt': vol_per_crtn, 'cbm': cbm, 'total_vol_wt': ttl_vol_wt, 'total_nwt_crtn': ttl_nwt_crtn, 'total_gwt_crtn': ttl_gwt_crtn})
			line.write({'toal_qty_carton': ttl_qty_crtn, 'vol_wt': vol_per_crtn,})
			print "+++CBM+++",line.cbm,line.toal_qty_carton
		return
		'''

	@api.model
	def create(self, vals):
		#print"-======--------====-----=========-----",vals,vals['product_tmpl_id']
		if 'product_tmpl_id' in vals:
			tpl = self.env['product.template'].search([('id','=',vals['product_tmpl_id'])])
			if tpl and tpl.attribute_line_ids:
				vals['item_code'] = tpl.attribute_line_ids[0].item_code
				vals['no_of_catons'] = tpl.attribute_line_ids[0].no_of_catons
				vals['net_weight'] = tpl.attribute_line_ids[0].net_weight
				vals['gross_weight'] = tpl.attribute_line_ids[0].gross_weight
				vals['no_of_item'] = tpl.attribute_line_ids[0].no_of_item
				vals['toal_qty_carton'] = tpl.attribute_line_ids[0].toal_qty_carton
				vals['carton_nwt'] = tpl.attribute_line_ids[0].carton_nwt
				vals['carton_gwt'] = tpl.attribute_line_ids[0].carton_gwt
				vals['x_attr'] = tpl.attribute_line_ids[0].x_attr
				vals['y_attr'] = tpl.attribute_line_ids[0].y_attr
				vals['z_attr'] = tpl.attribute_line_ids[0].z_attr
				vals['total_qty'] = tpl.attribute_line_ids[0].total_qty
				vals['cartons'] = tpl.attribute_line_ids[0].cartons
				vals['vol_wt'] = tpl.attribute_line_ids[0].vol_wt
				vals['cbm'] = tpl.attribute_line_ids[0].cbm
				vals['total_vol_wt'] = tpl.attribute_line_ids[0].total_vol_wt
				vals['total_nwt_crtn'] = tpl.attribute_line_ids[0].total_nwt_crtn
				vals['total_gwt_crtn'] = tpl.attribute_line_ids[0].total_gwt_crtn
		product = super(ProductProduct, self.with_context(create_product_product=True)).create(vals)
		# When a unique variant is created from tmpl then the standard price is set by _set_standard_price
		if not (self.env.context.get('create_from_tmpl') and len(product.product_tmpl_id.product_variant_ids) == 1):
			product._set_standard_price(vals.get('standard_price') or 0.0)
		return product


