from odoo import api, fields, models, _
from odoo.tools import amount_to_text_en, float_round
from datetime import datetime, timedelta
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT

class saleOrderGST(models.Model):
	_inherit="sale.order"

	@api.multi    
	def amount_to_text(self, amount, currency):
		convert_amount_in_words = amount_to_text_en.amount_to_text(amount, lang='en', currency='')        
		convert_amount_in_words = convert_amount_in_words.replace(' and Zero Cent', ' Only ')         
		return convert_amount_in_words

	via_freight = fields.Many2one('freight.to','Via Freight To')
	freight_charge = fields.Monetary('Freight & Insurance')
	bank_charge = fields.Monetary('Banking & Handling')
	full_total = fields.Monetary('Total Amount',compute='total_price')
	amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all', track_visibility='always')
	confirmation_date = fields.Date(string='Confirmation Date', readonly=True, index=True, help="Date on which the sale order is confirmed.", oldname="date_confirm")
	remarks =fields.Text('Remarks')
	buyer_ref = fields.Text('Buyer Reference')
	incoterms = fields.Many2one('incoterm.trade','Incoterm')
	delivery_time = fields.Many2one('delivered.time','Delivery Time')
	show_disc = fields.Boolean('Show Discount')
	global_disc = fields.Monetary('Discount')
	remarks1 =fields.Char('Remarks1')
	remarks2 =fields.Char('Remarks2')
	remarks3 =fields.Char('Remarks3')
	remarks4 =fields.Char('Remarks4')
	remarks5 =fields.Char('Remarks5')
	remarks6 =fields.Char('Remarks6')
	remarks7 =fields.Char('Remarks7')
	remarks8 =fields.Char('Remarks8')
	remarks9 =fields.Char('Remarks9')
	remarks10 =fields.Char('Remarks10')
	remarks11 =fields.Char('Remarks11')
	remarks12 =fields.Char('Remarks12')
    
#     @api.multi
#     def name_get(self):
#         print "Entery=="
#         if context is None:
#             context = {}
#         if isinstance(ids, (int, long)):
#             ids = [ids]
#         res = []
#         if context.get('special_display_name', False):
#             for record in self.browse(cr, uid, ids, context=context):
#                 amount_total = record.amount_total
#                 incoterm = record.self.incoterm
#                 res.append(record.id, amount_total + " - " + incoterm + "%")
#         else:
#             # Do a for and set here the standard display name, for example if the standard display name were name, you should do the next for
#             for record in self.browse(cr, uid, ids, context=context):
#                 res.append(record.id, record.amount_total)
#         return res
#     @api.multi
#     def name_get(self):
#         res = []
#         for asset in self:
#             display_name = []
#             res.append((asset.id,
#                     asset.amount_total + ' ' + asset.incoterm.name))
#             return res

	@api.onchange('amount_total')
	def total_price(self):
		for recs in self:
			recs.full_total =recs.amount_total+recs.freight_charge+recs.bank_charge - recs.global_disc
			print "full_total====",recs.full_total
		return

class incoterm_trade(models.Model):
    _name="incoterm.trade"
    
    name = fields.Char('INCOTERM')

class delivered_time(models.Model):
    _name="delivered.time"
    
    name= fields.Char("DELIVERY TIME")
    
class freight_to(models.Model):
    _name="freight.to"  
    _description="Freight To"
    
    name= fields.Char('Freight Name')
      
class account_invoice(models.Model):
    _inherit = "account.invoice"
    
    @api.multi    
    def amount_to_text(self, amount, currency):
        convert_amount_in_words = amount_to_text_en.amount_to_text(amount, lang='en', currency='')        
        convert_amount_in_words = convert_amount_in_words.replace(' and Zero Cent', ' Only ')         
        return convert_amount_in_words
    
class ProductAttributeLine(models.Model):
	_inherit = "product.attribute.line"

	item_code = fields.Char('Item Code')
	no_of_catons = fields.Integer('Primary Unit', required=True)
	net_weight = fields.Float('Pri. Net Weight')
	gross_weight = fields.Float('Pri. Gross Weight')
	no_of_item = fields.Integer('Unit in carton Qty.', required=True)
	toal_qty_carton = fields.Integer('Total Qty. in Carton', readonly=True)
	carton_nwt = fields.Float('Carton Net Weight')
	carton_gwt = fields.Float('Carton Gross Weight')
	x_attr = fields.Float('Len', required=True)
	y_attr = fields.Float('Breadth',required=True) 
	z_attr = fields.Float('Height',required=True)
	total_qty = fields.Float('Total Qty')
	cartons = fields.Float('Cartons')
	vol_wt = fields.Float('Unit carton CBM', readonly=True)
	cbm = fields.Float('CBM', readonly=True)
	total_vol_wt = fields.Float('Total Volume Weight')
	total_nwt_crtn = fields.Float('Total Net Weight Carton') 
	total_gwt_crtn = fields.Float('Total Gross Weight Carton') 

	#     x_attr = fields.Many2one('product.dimen', 'Dimension(Len)')
	#     y_attr = fields.Many2one('product.dimen','Dimension(B)')

	@api.onchange('value_ids')
	def onchange_attvalue(self):
		print"-----------99999999999--------",self.item_code,self.product_tmpl_id.id
		tmpl = self.env['product.template'].search([('name','=',self.product_tmpl_id.name)])
		prod = self.env['product.product'].search([('product_tmpl_id','=',tmpl.id)])
		print"--prod---------prod--",prod
		for p in prod:
			print"00000000000000000000000000",p.item_code
			p.write({'item_code': self.item_code, 'no_of_catons': self.no_of_catons, 'net_weight': self.net_weight,
				'gross_weight': self.gross_weight, 'no_of_item': self.no_of_item, 'toal_qty_carton': self.toal_qty_carton,
				'carton_nwt': self.carton_nwt, 'carton_gwt': self.carton_gwt, 'x_attr': self.x_attr, 'y_attr': self.y_attr,
				'z_attr': self.z_attr, 'total_qty': self.total_qty, 'cartons': self.cartons, 'vol_wt': self.vol_wt,
				'cbm': self.cbm, 'total_vol_wt': self.total_vol_wt, 'total_nwt_crtn': self.total_nwt_crtn,
				'total_gwt_crtn': self.total_gwt_crtn
			})
			


    
class ProductTemplate(models.Model):
	_inherit = 'product.template'

	no_of_item = fields.Integer('No. Of Items in 1 carton')
	comp = fields.Char(compute="calculate_cbm", string="Calc. CBM")

	@api.multi
	def calculate_cbm(self):
		print "ENTRY=---"
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
    
# class ProductDimen(models.Model):
#     _name = "product.dimen"
#     
#     name = fields.Char('Name')
    
    
    
    
    
    
    
    
    
