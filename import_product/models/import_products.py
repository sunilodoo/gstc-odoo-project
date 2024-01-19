# -*- coding: utf-8 -*-
from openerp import models, fields, osv, api, _
from openerp.tools.translate import _
from openerp import tools, api
from openerp import SUPERUSER_ID
from datetime import datetime, timedelta
import csv
import tempfile
import StringIO
import base64
import datetime as dt
from openerp.exceptions import Warning
import logging

_logger = logging.getLogger(__name__)


class import_products(models.TransientModel):
	_name = 'import.products'

	product_file = fields.Binary(string='CSV File', help='File should be separated by comma (,) and quoted using Quote character (") ')
	
	@api.multi
	def do_import(self):
		print"========================",self
		partner_pool = self.env['res.partner']
		prod_pool = self.env['product.template']
		attrib_pool = self.env['product.attribute']
		attrib_vl_pool = self.env['product.attribute.value']
		user_pool  = self.env['res.users']
		categ_pool  = self.env['product.category']

		f = StringIO.StringIO(base64.decodestring(self.product_file))
		reader = csv.reader(f, delimiter=',')
		
		headers = {}
		for row in reader:
			col_count = 0
			for col in row:
				headers[col] = col_count
				col_count = col_count + 1
			break;
		count = 1
		for row in reader:
			# print"=============2222222222===================",row[headers['Item Name']].strip()
			count = count + 1
			# prod_vals = {
			# 		            'name' : row[headers['Item Name']].strip(),
	        #                     'description'   : row[headers['Item Desc']].strip(),
	        #                     'type'    : "product",
	                            
			# }
			attr2_id = ''
			attr3_id = ''
			attr4_id = ''
			attr5_id = ''
			attr6_id = ''

			attr7_id = ''
			attr8_id = ''
			attr9_id = ''
			attr10_id = ''
			attr11id = ''

			attr12_id = ''
			attr13_id = ''
			attr14_id = ''
			attr15_id = ''
			attr16_id = ''

			attr17_id = ''
			attr18_id = ''
			attr19_id = ''
			attr20_id = ''
			attr21_id = ''

			if row[headers['Categ']]:
				part = row[headers['Categ']].strip()
				part1 = row[headers['Sub-categ']].strip()
				part_ids = categ_pool.search([('name','=',part1)])
				if part_ids:
					part_id = part_ids[0]
				else:
					part_id = categ_pool.create({'name': part1})

				prod_vals['categ_id'] = part_id.id 
				
			
			if row[headers['Attribute']]:
				attr1 = row[headers['Attribute']].strip()
				attr1_ids = attrib_pool.search([('name','=',attr1)])
				if attr1_ids:
					attr1_id = attr1_ids[0]
				else:
					attr1_id = attrib_pool.create({'name': attr1})

			if row[headers['Attribute value']]:
				attr2 = row[headers['Attribute value']].strip()
				attr2_ids = attrib_vl_pool.search([('name','=',attr2)])
				if attr2_ids:
					attr2_id = attr2_ids[0]
				else:
					attr2_id = attrib_vl_pool.create({'attribute_id': attr1_id.id,'name': attr2})
			
			if row[headers['Attribute value2']]:
				attr3 = row[headers['Attribute value2']].strip()
				attr3_ids = attrib_vl_pool.search([('name','=',attr3)])
				if attr3_ids:
					attr3_id = attr3_ids[0]
				else:
					attr3_id = attrib_vl_pool.create({'attribute_id': attr1_id.id,'name': attr3})

			if row[headers['Attribute value3']]:
				attr4 = row[headers['Attribute value3']].strip()
				attr4_ids = attrib_vl_pool.search([('name','=',attr4)])
				if attr4_ids:
					attr4_id = attr4_ids[0]
				else:
					attr4_id = attrib_vl_pool.create({'attribute_id': attr1_id.id,'name': attr4})

			if row[headers['Attribute value4']]:
				attr5 = row[headers['Attribute value4']].strip()
				attr5_ids = attrib_vl_pool.search([('name','=',attr5)])
				if attr5_ids:
					attr5_id = attr5_ids[0]
				else:
					attr5_id = attrib_vl_pool.create({'attribute_id': attr1_id.id,'name': attr5})

			if row[headers['Attribute value5']]:
				attr6 = row[headers['Attribute value5']].strip()
				attr6_ids = attrib_vl_pool.search([('name','=',attr6)])
				if attr6_ids:
					attr6_id = attr6_ids[0]
				else:
					attr6_id = attrib_vl_pool.create({'attribute_id': attr1_id.id,'name': attr6})

			
			if row[headers['Attribute value6']]:
				attr7 = row[headers['Attribute value6']].strip()
				attr7_ids = attrib_vl_pool.search([('name','=',attr7)])
				if attr7_ids:
					attr7_id = attr7_ids[0]
				else:
					attr7_id = attrib_vl_pool.create({'attribute_id': attr1_id.id,'name': attr7})
			
			if row[headers['Attribute value7']]:
				attr8 = row[headers['Attribute value7']].strip()
				attr8_ids = attrib_vl_pool.search([('name','=',attr8)])
				if attr8_ids:
					attr8_id = attr8_ids[0]
				else:
					attr8_id = attrib_vl_pool.create({'attribute_id': attr1_id.id,'name': attr8})

			if row[headers['Attribute value8']]:
				attr9 = row[headers['Attribute value8']].strip()
				attr9_ids = attrib_vl_pool.search([('name','=',attr9)])
				if attr9_ids:
					attr9_id = attr9_ids[0]
				else:
					attr9_id = attrib_vl_pool.create({'attribute_id': attr1_id.id,'name': attr9})

			if row[headers['Attribute value9']]:
				attr10 = row[headers['Attribute value9']].strip()
				attr10_ids = attrib_vl_pool.search([('name','=',attr10)])
				if attr10_ids:
					attr10_id = attr10_ids[0]
				else:
					attr10_id = attrib_vl_pool.create({'attribute_id': attr1_id.id,'name': attr10})

			if row[headers['Attribute value10']]:
				attr11 = row[headers['Attribute value10']].strip()
				attr11_ids = attrib_vl_pool.search([('name','=',attr11)])
				if attr11_ids:
					attr11_id = attr11_ids[0]
				else:
					attr11_id = attrib_vl_pool.create({'attribute_id': attr1_id.id,'name': attr11})


			if row[headers['Attribute value11']]:
				attr12 = row[headers['Attribute value11']].strip()
				attr12_ids = attrib_vl_pool.search([('name','=',attr12)])
				if attr12_ids:
					attr12_id = attr12_ids[0]
				else:
					attr12_id = attrib_vl_pool.create({'attribute_id': attr1_id.id,'name': attr12})
			
			if row[headers['Attribute value12']]:
				attr13 = row[headers['Attribute value12']].strip()
				attr13_ids = attrib_vl_pool.search([('name','=',attr13)])
				if attr13_ids:
					attr13_id = attr13_ids[0]
				else:
					attr13_id = attrib_vl_pool.create({'attribute_id': attr1_id.id,'name': attr13})

			if row[headers['Attribute value13']]:
				attr14 = row[headers['Attribute value13']].strip()
				attr14_ids = attrib_vl_pool.search([('name','=',attr14)])
				if attr14_ids:
					attr14_id = attr14_ids[0]
				else:
					attr14_id = attrib_vl_pool.create({'attribute_id': attr1_id.id,'name': attr14})

			if row[headers['Attribute value14']]:
				attr15 = row[headers['Attribute value14']].strip()
				attr15_ids = attrib_vl_pool.search([('name','=',attr15)])
				if attr15_ids:
					attr15_id = attr15_ids[0]
				else:
					attr15_id = attrib_vl_pool.create({'attribute_id': attr1_id.id,'name': attr15})

			if row[headers['Attribute value15']]:
				attr16 = row[headers['Attribute value15']].strip()
				attr16_ids = attrib_vl_pool.search([('name','=',attr16)])
				if attr16_ids:
					attr16_id = attr16_ids[0]
				else:
					attr16_id = attrib_vl_pool.create({'attribute_id': attr1_id.id,'name': attr16})


			if row[headers['Attribute value16']]:
				attr17 = row[headers['Attribute value16']].strip()
				attr17_ids = attrib_vl_pool.search([('name','=',attr17)])
				if attr17_ids:
					attr17_id = attr17_ids[0]
				else:
					attr17_id = attrib_vl_pool.create({'attribute_id': attr1_id.id,'name': attr17})
			
			if row[headers['Attribute value17']]:
				attr18 = row[headers['Attribute value17']].strip()
				attr18_ids = attrib_vl_pool.search([('name','=',attr18)])
				if attr18_ids:
					attr18_id = attr18_ids[0]
				else:
					attr18_id = attrib_vl_pool.create({'attribute_id': attr1_id.id,'name': attr18})

			if row[headers['Attribute value18']]:
				attr19 = row[headers['Attribute value18']].strip()
				attr19_ids = attrib_vl_pool.search([('name','=',attr19)])
				if attr19_ids:
					attr19_id = attr19_ids[0]
				else:
					attr19_id = attrib_vl_pool.create({'attribute_id': attr1_id.id,'name': attr19})

			if row[headers['Attribute value19']]:
				attr20 = row[headers['Attribute value19']].strip()
				attr20_ids = attrib_vl_pool.search([('name','=',attr20)])
				if attr20_ids:
					attr20_id = attr20_ids[0]
				else:
					attr20_id = attrib_vl_pool.create({'attribute_id': attr1_id.id,'name': attr20})

			if row[headers['Attribute value20']]:
				attr21 = row[headers['Attribute value20']].strip()
				attr21_ids = attrib_vl_pool.search([('name','=',attr21)])
				if attr21_ids:
					attr21_id = attr21_ids[0]
				else:
					attr21_id = attrib_vl_pool.create({'attribute_id': attr1_id.id,'name': attr21})
				#prod_vals['attribute_line_ids'] = attr1_id.id 

			print"====----------===============",attr2_id,attr3_id,attr4_id,attr5_id,attr6_id
			'''
			if row[headers['System Type']]:
				attr2 = row[headers['System Type']].strip()
				attr2_ids = attrib_pool.search([('name','=',attr2)])
				if attr2_ids:
					attr2_id = attr2_ids[0]
				else:
					attr2_id = attrib_pool.create({'name': attr2})

				prod_vals['attribute_line_ids'] = attr2_id.id 
			
			if row[headers['Version']]:
				attr3 = row[headers['System Type']].strip()
				attr3_ids = categ_pool.search([('name','=',attr3)])
				if attr3_ids:
					attr3_id = attr3_ids[0]
				else:
					attr3_id = categ_pool.create({'name': attr3})

				prod_vals['attribute_line_ids'] = attr3_id.id 
			'''
			print"-----------------------------",prod_vals
			'''
			if row[headers['CONTACT NAME']]:
				print"===============",row[headers['CONTACT NAME']].strip()
				child = row[headers['CONTACT NAME']].strip()
				child_ids = partner_pool.search([('name','=',child)])
				if child_ids:
					child_ids = child_ids[0]
				else:
					child_ids = partner_pool.create({'child_ids': [(0,0, {'name': row[headers['CONTACT NAME']].strip(), 'function': row[headers['CONTACT POSITION']].strip()})]})

				prod_vals['child_ids'] = child_ids.id
			if row[headers['SALESPERSON']]:
				user = row[headers['SALESPERSON']].strip()
				user_ids = user_pool.search([('name','=',user)])
				if user_ids:
					user_id = user_ids[0]
				else:
					user_id = user_pool.create({'name': user,'login': user})

				prod_vals['user_id'] = user_id.id
				
			if row[headers['SALESTEAM']]:
				section = row[headers['SALESTEAM']].strip()
				section_ids = crm_pool.search([('name','=',section)])
				if section_ids:
					section_id = section_ids[0]
				else:
					section_id = crm_pool.create({'name': section})

				prod_vals['section_id'] = section_id.id

			if row[headers['STATE']]:
				state = row[headers['STATE']].strip()
				state_ids = state_pool.search([('code','=',state)])
				if state_ids:
					state_id = state_ids[0]
				else:
					state_id = state_pool.create({'name': state, 'code':state[:2], 'country_id': prod_vals.get('country_id', 105)})

				prod_vals['state_id'] = state_id.id
			'''
			#print"=====================================",attr2_id.id,attr2_id.name,attr2_id.attribute_id,attr2_id.attribute_id.name
			product_exists = prod_pool.search([('name','=',row[headers['Item Name']].strip())])
			if not product_exists:
				product_id = prod_pool.create(prod_vals)
				if attr2_id and not attr3_id:
					print"=======attr2_id-----ye====="
					product_id.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})
				if attr2_id and attr3_id and not attr4_id:
					print"=======attr2_id--&attr3_id---ye====="
					product_id.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})
				if attr2_id and attr3_id and attr4_id and not attr5_id:
					print"=======attr2_id--&attr3_id-&==attr4--ye====="
					product_id.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})
				if attr2_id and attr3_id and attr4_id and attr5_id and not attr6_id:
					print"=======attr2_id--&attr3_id-&==attr4-====attr5-ye====="
					product_id.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id,attr5_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})
				if attr2_id and attr3_id and attr4_id and attr5_id and attr6_id and not attr7_id:
					print"=======attr2_id--&attr3_id-&==attr4-====attr6-ye====="
					product_id.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id,attr5_id.id,attr6_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})
				
				if attr2_id and attr3_id and attr4_id and attr5_id and attr6_id and attr7_id and not attr8_id:
					print"=======attr2_id--&attr3_id-&==attr4-====attr6-ye====="
					product_id.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id,attr5_id.id,attr6_id.id,attr7_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})

				if attr2_id and attr3_id and attr4_id and attr5_id and attr6_id and attr7_id and attr8_id and not attr9_id:
					print"=======attr2_id--&attr3_id-&==attr4-====attr6-ye====="
					product_id.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id,attr5_id.id,attr6_id.id,attr7_id.id,attr8_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})

				if attr2_id and attr3_id and attr4_id and attr5_id and attr6_id and attr7_id and attr8_id and attr9_id and not attr10_id:
					print"=======attr2_id--&attr3_id-&==attr4-====attr6-ye====="
					product_id.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id,attr5_id.id,attr6_id.id,attr7_id.id,attr8_id.id,attr9_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})

				if attr2_id and attr3_id and attr4_id and attr5_id and attr6_id and attr7_id and attr8_id and attr9_id and attr10_id and not attr11_id:
					print"=======attr2_id--&attr3_id-&==attr4-====attr6-ye====="
					product_id.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id,attr5_id.id,attr6_id.id,attr7_id.id,attr8_id.id,attr9_id.id,attr10_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})

				if attr2_id and attr3_id and attr4_id and attr5_id and attr6_id and attr7_id and attr8_id and attr9_id and attr10_id and attr11_id and not attr12_id:
					print"=======attr2_id--&attr3_id-&==attr4-====attr6-ye====="
					product_id.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id,attr5_id.id,attr6_id.id,attr7_id.id,attr8_id.id,attr9_id.id,attr10_id.id,attr11_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})
				
				if attr2_id and attr3_id and attr4_id and attr5_id and attr6_id and attr7_id and attr8_id and attr9_id and attr10_id and attr11_id and attr12_id and not attr13_id:
					print"=======attr2_id--&attr3_id-&==attr4-====attr6-ye====="
					product_id.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id,attr5_id.id,attr6_id.id,attr7_id.id,attr8_id.id,attr9_id.id,attr10_id.id,attr11_id.id,attr12_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})

				if attr2_id and attr3_id and attr4_id and attr5_id and attr6_id and attr7_id and attr8_id and attr9_id and attr10_id and attr11_id and attr12_id and attr13_id and not attr14_id:
					print"=======attr2_id--&attr3_id-&==attr4-====attr6-ye====="
					product_id.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id,attr5_id.id,attr6_id.id,attr7_id.id,attr8_id.id,attr9_id.id,attr10_id.id,attr11_id.id,attr12_id.id,attr13_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})


				if attr2_id and attr3_id and attr4_id and attr5_id and attr6_id and attr7_id and attr8_id and attr9_id and attr10_id and attr11_id and attr12_id and attr13_id and attr14_id and not attr15_id:
					print"=======attr2_id--&attr3_id-&==attr4-====attr6-ye====="
					product_id.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id,attr5_id.id,attr6_id.id,attr7_id.id,attr8_id.id,attr9_id.id,attr10_id.id,attr11_id.id,attr12_id.id,attr13_id.id,attr14_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})

				if attr2_id and attr3_id and attr4_id and attr5_id and attr6_id and attr7_id and attr8_id and attr9_id and attr10_id and attr11_id and attr12_id and attr13_id and attr14_id and attr15_id and not attr16_id:
					print"=======attr2_id--&attr3_id-&==attr4-====attr6-ye====="
					product_id.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id,attr5_id.id,attr6_id.id,attr7_id.id,attr8_id.id,attr9_id.id,attr10_id.id,attr11_id.id,attr12_id.id,attr13_id.id,attr14_id.id,attr15_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})

				if attr2_id and attr3_id and attr4_id and attr5_id and attr6_id and attr7_id and attr8_id and attr9_id and attr10_id and attr11_id and attr12_id and attr13_id and attr14_id and attr15_id and attr16_id and not attr17_id:
					print"=======attr2_id--&attr3_id-&==attr4-====attr6-ye====="
					product_id.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id,attr5_id.id,attr6_id.id,attr7_id.id,attr8_id.id,attr9_id.id,attr10_id.id,attr11_id.id,attr12_id.id,attr13_id.id,attr14_id.id,attr15_id.id,attr16_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})


				if attr2_id and attr3_id and attr4_id and attr5_id and attr6_id and attr7_id and attr8_id and attr9_id and attr10_id and attr11_id and attr12_id and attr13_id and attr14_id and attr15_id and attr16_id and attr17_id and not attr18_id:
					print"=======attr2_id--&attr3_id-&==attr4-====attr6-ye====="
					product_id.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id,attr5_id.id,attr6_id.id,attr7_id.id,attr8_id.id,attr9_id.id,attr10_id.id,attr11_id.id,attr12_id.id,attr13_id.id,attr14_id.id,attr15_id.id,attr16_id.id,attr17_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})


				if attr2_id and attr3_id and attr4_id and attr5_id and attr6_id and attr7_id and attr8_id and attr9_id and attr10_id and attr11_id and attr12_id and attr13_id and attr14_id and attr15_id and attr16_id and attr17_id and attr18_id and not attr19_id:
					print"=======attr2_id--&attr3_id-&==attr4-====attr6-ye====="
					product_id.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id,attr5_id.id,attr6_id.id,attr7_id.id,attr8_id.id,attr9_id.id,attr10_id.id,attr11_id.id,attr12_id.id,attr13_id.id,attr14_id.id,attr15_id.id,attr16_id.id,attr17_id.id,attr18_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})

				if attr2_id and attr3_id and attr4_id and attr5_id and attr6_id and attr7_id and attr8_id and attr9_id and attr10_id and attr11_id and attr12_id and attr13_id and attr14_id and attr15_id and attr16_id and attr17_id and attr18_id and attr19_id and not attr20_id:
					print"=======attr2_id--&attr3_id-&==attr4-====attr6-ye====="
					product_id.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id,attr5_id.id,attr6_id.id,attr7_id.id,attr8_id.id,attr9_id.id,attr10_id.id,attr11_id.id,attr12_id.id,attr13_id.id,attr14_id.id,attr15_id.id,attr16_id.id,attr17_id.id,attr18_id.id,attr19_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})


				if attr2_id and attr3_id and attr4_id and attr5_id and attr6_id and attr7_id and attr8_id and attr9_id and attr10_id and attr11_id and attr12_id and attr13_id and attr14_id and attr15_id and attr16_id and attr17_id and attr18_id and attr19_id and attr20_id and not attr21_id:
					print"=======attr2_id--&attr3_id-&==attr4-====attr6-ye====="
					product_id.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id,attr5_id.id,attr6_id.id,attr7_id.id,attr8_id.id,attr9_id.id,attr10_id.id,attr11_id.id,attr12_id.id,attr13_id.id,attr14_id.id,attr15_id.id,attr16_id.id,attr17_id.id,attr18_id.id,attr19_id.id,attr20_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})

				if attr2_id and attr3_id and attr4_id and attr5_id and attr6_id and attr7_id and attr8_id and attr9_id and attr10_id and attr11_id and attr12_id and attr13_id and attr14_id and attr15_id and attr16_id and attr17_id and attr18_id and attr19_id and attr20_id and attr21_id:
					print"=======attr2_id--&attr3_id-&==attr4-====attr6-ye====="
					product_id.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id,attr5_id.id,attr6_id.id,attr7_id.id,attr8_id.id,attr9_id.id,attr10_id.id,attr11_id.id,attr12_id.id,attr13_id.id,attr14_id.id,attr15_id.id,attr16_id.id,attr17_id.id,attr18_id.id,attr19_id.id,attr20_id.id,attr21_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})

				print"==========product_id======Created==============",product_id
			else:
				print"==========product_exists=================",product_exists.attribute_line_ids
				
				if attr2_id and not attr3_id:
					print"=======attr2_id-----ye====="
					product_exists.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})
				if attr2_id and attr3_id and not attr4_id:
					print"=======attr2_id--&attr3_id---ye====="
					product_exists.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})
				if attr2_id and attr3_id and attr4_id and not attr5_id:
					print"=======attr2_id--&attr3_id-&==attr4--ye====="
					product_exists.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})
				if attr2_id and attr3_id and attr4_id and attr5_id and not attr6_id:
					print"=======attr2_id--&attr3_id-&==attr4-====attr5-ye====="
					product_exists.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id,attr5_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})
				if attr2_id and attr3_id and attr4_id and attr5_id and attr6_id and not attr7_id:
					print"=======attr2_id--&attr3_id-&==attr4-====attr6-ye====="
					product_exists.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id,attr5_id.id,attr6_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})

				if attr2_id and attr3_id and attr4_id and attr5_id and attr6_id and attr7_id and not attr8_id:
					print"=======attr2_id--&attr3_id-&==attr4-====attr6-ye====="
					product_exists.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id,attr5_id.id,attr6_id.id,attr7_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})

				if attr2_id and attr3_id and attr4_id and attr5_id and attr6_id and attr7_id and attr8_id and not attr9_id:
					print"=======attr2_id--&attr3_id-&==attr4-====attr6-ye====="
					product_exists.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id,attr5_id.id,attr6_id.id,attr7_id.id,attr8_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})

				if attr2_id and attr3_id and attr4_id and attr5_id and attr6_id and attr7_id and attr8_id and attr9_id and not attr10_id:
					print"=======attr2_id--&attr3_id-&==attr4-====attr6-ye====="
					product_exists.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id,attr5_id.id,attr6_id.id,attr7_id.id,attr8_id.id,attr9_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})

				if attr2_id and attr3_id and attr4_id and attr5_id and attr6_id and attr7_id and attr8_id and attr9_id and attr10_id and not attr11_id:
					print"=======attr2_id--&attr3_id-&==attr4-====attr6-ye====="
					product_exists.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id,attr5_id.id,attr6_id.id,attr7_id.id,attr8_id.id,attr9_id.id,attr10_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})

				if attr2_id and attr3_id and attr4_id and attr5_id and attr6_id and attr7_id and attr8_id and attr9_id and attr10_id and attr11_id and not attr12_id:
					print"=======attr2_id--&attr3_id-&==attr4-====attr6-ye====="
					product_exists.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id,attr5_id.id,attr6_id.id,attr7_id.id,attr8_id.id,attr9_id.id,attr10_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})
				
				if attr2_id and attr3_id and attr4_id and attr5_id and attr6_id and attr7_id and attr8_id and attr9_id and attr10_id and attr11_id and attr12_id and not attr13_id:
					print"=======attr2_id--&attr3_id-&==attr4-====attr6-ye====="
					product_exists.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id,attr5_id.id,attr6_id.id,attr7_id.id,attr8_id.id,attr9_id.id,attr10_id.id,attr11_id.id,attr12_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})

				if attr2_id and attr3_id and attr4_id and attr5_id and attr6_id and attr7_id and attr8_id and attr9_id and attr10_id and attr11_id and attr12_id and attr13_id and not attr14_id:
					print"=======attr2_id--&attr3_id-&==attr4-====attr6-ye====="
					product_exists.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id,attr5_id.id,attr6_id.id,attr7_id.id,attr8_id.id,attr9_id.id,attr10_id.id,attr11_id.id,attr12_id.id,attr13_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})


				if attr2_id and attr3_id and attr4_id and attr5_id and attr6_id and attr7_id and attr8_id and attr9_id and attr10_id and attr11_id and attr12_id and attr13_id and attr14_id and not attr15_id:
					print"=======attr2_id--&attr3_id-&==attr4-====attr6-ye====="
					product_exists.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id,attr5_id.id,attr6_id.id,attr7_id.id,attr8_id.id,attr9_id.id,attr10_id.id,attr11_id.id,attr12_id.id,attr13_id.id,attr14_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})

				if attr2_id and attr3_id and attr4_id and attr5_id and attr6_id and attr7_id and attr8_id and attr9_id and attr10_id and attr11_id and attr12_id and attr13_id and attr14_id and attr15_id and not attr16_id:
					print"=======attr2_id--&attr3_id-&==attr4-====attr6-ye====="
					product_exists.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id,attr5_id.id,attr6_id.id,attr7_id.id,attr8_id.id,attr9_id.id,attr10_id.id,attr11_id.id,attr12_id.id,attr13_id.id,attr14_id.id,attr15_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})

				if attr2_id and attr3_id and attr4_id and attr5_id and attr6_id and attr7_id and attr8_id and attr9_id and attr10_id and attr11_id and attr12_id and attr13_id and attr14_id and attr15_id and attr16_id and not attr17_id:
					print"=======attr2_id--&attr3_id-&==attr4-====attr6-ye====="
					product_exists.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id,attr5_id.id,attr6_id.id,attr7_id.id,attr8_id.id,attr9_id.id,attr10_id.id,attr11_id.id,attr12_id.id,attr13_id.id,attr14_id.id,attr15_id.id,attr16_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})


				if attr2_id and attr3_id and attr4_id and attr5_id and attr6_id and attr7_id and attr8_id and attr9_id and attr10_id and attr11_id and attr12_id and attr13_id and attr14_id and attr15_id and attr16_id and attr17_id and not attr18_id:
					print"=======attr2_id--&attr3_id-&==attr4-====attr6-ye====="
					product_exists.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id,attr5_id.id,attr6_id.id,attr7_id.id,attr8_id.id,attr9_id.id,attr10_id.id,attr11_id.id,attr12_id.id,attr13_id.id,attr14_id.id,attr15_id.id,attr16_id.id,attr17_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})


				if attr2_id and attr3_id and attr4_id and attr5_id and attr6_id and attr7_id and attr8_id and attr9_id and attr10_id and attr11_id and attr12_id and attr13_id and attr14_id and attr15_id and attr16_id and attr17_id and attr18_id and not attr19_id:
					print"=======attr2_id--&attr3_id-&==attr4-====attr6-ye====="
					product_exists.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id,attr5_id.id,attr6_id.id,attr7_id.id,attr8_id.id,attr9_id.id,attr10_id.id,attr11_id.id,attr12_id.id,attr13_id.id,attr14_id.id,attr15_id.id,attr16_id.id,attr17_id.id,attr18_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})

				if attr2_id and attr3_id and attr4_id and attr5_id and attr6_id and attr7_id and attr8_id and attr9_id and attr10_id and attr11_id and attr12_id and attr13_id and attr14_id and attr15_id and attr16_id and attr17_id and attr18_id and attr19_id and not attr20_id:
					print"=======attr2_id--&attr3_id-&==attr4-====attr6-ye====="
					product_exists.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id,attr5_id.id,attr6_id.id,attr7_id.id,attr8_id.id,attr9_id.id,attr10_id.id,attr11_id.id,attr12_id.id,attr13_id.id,attr14_id.id,attr15_id.id,attr16_id.id,attr17_id.id,attr18_id.id,attr19_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})


				if attr2_id and attr3_id and attr4_id and attr5_id and attr6_id and attr7_id and attr8_id and attr9_id and attr10_id and attr11_id and attr12_id and attr13_id and attr14_id and attr15_id and attr16_id and attr17_id and attr18_id and attr19_id and attr20_id and not attr21_id:
					print"=======attr2_id--&attr3_id-&==attr4-====attr6-ye====="
					product_exists.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id,attr5_id.id,attr6_id.id,attr7_id.id,attr8_id.id,attr9_id.id,attr10_id.id,attr11_id.id,attr12_id.id,attr13_id.id,attr14_id.id,attr15_id.id,attr16_id.id,attr17_id.id,attr18_id.id,attr19_id.id,attr20_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})

				if attr2_id and attr3_id and attr4_id and attr5_id and attr6_id and attr7_id and attr8_id and attr9_id and attr10_id and attr11_id and attr12_id and attr13_id and attr14_id and attr15_id and attr16_id and attr17_id and attr18_id and attr19_id and attr20_id and attr21_id:
					print"=======attr2_id--&attr3_id-&==attr4-====attr6-ye====="
					product_exists.write({'categ_id':part_id.id, 'attribute_line_ids': [(0,0, {'attribute_id': attr1_id.id,'value_ids':[(6, 0, [attr2_id.id,attr3_id.id,attr4_id.id,attr5_id.id,attr6_id.id,attr7_id.id,attr8_id.id,attr9_id.id,attr10_id.id,attr11_id.id,attr12_id.id,attr13_id.id,attr14_id.id,attr15_id.id,attr16_id.id,attr17_id.id,attr18_id.id,attr19_id.id,attr20_id.id,attr21_id.id])], 'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(),})]})

			print"==========product_id======Created=====last=========",product_id
			new_prod = self.env['product.product'].search([('product_tmpl_id','=',product_id.id)])
			ttl_qty_crtn = 0
			vol_per_crtn = 0.0
			if row[headers['Pri. Unit']].strip() and row[headers['Unit in crtn']].strip():
				ttl_qty_crtn = int(row[headers['Pri. Unit']].strip()) * int(row[headers['Unit in crtn']].strip())
			if (row[headers['Length']].strip()) and (row[headers['Breadth']].strip()) and (row[headers['Height']].strip()): 
				vol_per_crtn = (float((row[headers['Length']].strip())) * float((row[headers['Breadth']].strip())) * float(row[headers['Height']].strip()))/1000000
			new_prod.write({'item_code': row[headers['Item code']].strip(), 'no_of_catons': row[headers['Pri. Unit']].strip(), 'net_weight': row[headers['Pri. Ntwt']].strip(), 'gross_weight': row[headers['Pri. Grwt']].strip(), 'no_of_item': row[headers['Unit in crtn']].strip(), 'toal_qty_carton': ttl_qty_crtn, 'carton_nwt': row[headers['Crtn Ntwt']].strip(), 'carton_gwt': row[headers['Crtn Grwt']].strip(), 'x_attr': row[headers['Length']].strip(), 'y_attr': row[headers['Breadth']].strip(), 'z_attr': row[headers['Height']].strip(), 'vol_wt': vol_per_crtn})
			print"==========product_id======product.product=====new_prod=========",new_prod

import_products()
