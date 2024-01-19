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


class import_customers(models.TransientModel):
	_name = 'import.customers'

	partner_file = fields.Binary(string='CSV File', help='File should be separated by comma (,) ')
	
	@api.multi
	def import_customer(self):

		partner_pool = self.env['res.partner']
		country_pool = self.env['res.country']
		state_pool = self.env['res.country.state']
		user_pool  = self.env['res.users']
		tagg_pool  = self.env['res.partner.category']
		classification_pool  = self.env['customer.classify']
		profile_pool  = self.env['company.profile']
		interest_pool  = self.env['product.interest']

		f = StringIO.StringIO(base64.decodestring(self.partner_file))
		reader = csv.reader(f, delimiter=',')
		#print"----------p--------====-partner_file------",self.partner_file
		headers = {}
		for row in reader:
			col_count = 0
			for col in row:
				headers[col] = col_count
				col_count = col_count + 1
			break;
		count = 1
		for row in reader:
			print"=============2222222222===================",row[headers['CUSTOMER']]
			count = count + 1
			#if not row[headers['CONTACT NAME']]:
			partner_vals = {
					            'is_company' : True,
								#'old_customer': True,
								'customer': True,
					            'name' : row[headers['CUSTOMER']].strip(),
	                            'email'   : row[headers['EMAIL']].strip(),
	                            'street'  : row[headers['STREET']].strip(),
	                            'street2'  : row[headers['STREET2']].strip(),
	                            'city'    : row[headers['REGION']].strip(),
	                            'zip'     : row[headers['PCODE']].strip(),
	                            'phone'   : row[headers['PHONE']].strip(),
	                            'fax'   : row[headers['FAX']].strip(),
	                            #'name_1'   : row[headers['CONTACT NAME']].strip(),
	                            #'function'   : row[headers['CONTACT POSITION']].strip(),
	                            'child_ids': [(0,0, {'name': row[headers['CONTACT NAME']].strip()})],
	                            'website': row[headers['Website']].strip(),
	                            'mobile': row[headers['MOBILE']].strip(),
			}
			
		
			partner_vals['state_id'] = ''
			if row[headers['STATE']]:
				state = row[headers['STATE']].strip()
				state_ids = state_pool.search([('name','=',state)])
				if state_ids:
					state_id = state_ids[0]
				else:
					state_id = ''

				partner_vals['state_id'] = state_id and state_id.id or ''
		
			partner_vals['country_id'] = ''
			if row[headers['COUNTRY']]:
				country = row[headers['COUNTRY']].strip()
				country_ids = country_pool.search([('name','=',country.capitalize())])
				if country_ids:
					country_id = country_ids[0]
				else:
					raise Warning(_("Country not defined! "+country))

				partner_vals['country_id'] = country_id.id

			partner_vals['category_id'] = ''
			if row[headers['Tagging']]:
				tagging = row[headers['Tagging']].strip()
				tagging_ids = tagg_pool.search([('name','=',tagging)])
				if tagging_ids:
					tagging_id = tagging_ids[0]

				partner_vals['category_id'] = [(6, 0, [tagging_id.id])]

			partner_vals['classification_id'] = ''
			if row[headers['classification']]:
				classification = row[headers['classification']].strip()
				classification_ids = classification_pool.search([('name','=',classification)])
				if classification_ids:
					classification_id = classification_ids[0]

				partner_vals['classification_id'] = classification_ids.id

			partner_vals['user_id'] = ''
			if row[headers['salesperson']]:
				salesperson = row[headers['salesperson']].strip()
				salesperson_ids = classification_pool.search([('name','=',salesperson)])
				if salesperson_ids:
					salesperson_id = salesperson_ids[0]

				partner_vals['user_id'] = salesperson_ids.id

			partner_vals['company_profile'] = ''
			if row[headers['Company profile']]:
				profile = row[headers['Company profile']].strip()
				profile_ids = profile_pool.search([('name','=',profile)])
				if profile_ids:
					profile_id = profile_ids[0]

				partner_vals['company_profile'] = [(6, 0, [profile_id.id])]

			partner_vals['product_interest'] = ''
			if row[headers['products of interest']]:
				interest = row[headers['products of interest']].strip()
				interest_ids = interest_pool.search([('name','=',interest)])
				if interest_ids:
					interest_id = interest_ids[0]

				partner_vals['product_interest'] = [(6, 0, [interest_id.id])]

			print"==========Partner======Created==============",partner_vals
			partner_exists = partner_pool.search([('name','=',row[headers['CUSTOMER']].strip())])
			if not partner_exists:
				partner_id = partner_pool.create(partner_vals)
				print"==========Partner======Created=============="
			else:
				partner_exists.write({'country_id': partner_vals['country_id'], 'email': partner_vals['email'], 'phone': partner_vals['phone'], 'mobile': partner_vals['mobile'], 'website': partner_vals['website'], 'category_id': partner_vals['category_id'], 'classification_id': partner_vals['classification_id'], 'user_id': partner_vals['user_id'], 'company_profile': partner_vals['company_profile'], 'product_interest': partner_vals['product_interest']})


	@api.multi
	def update_customer(self):

		partner_pool = self.env['res.partner']
		user_pool  = self.env['res.users']

		f = StringIO.StringIO(base64.decodestring(self.partner_file))
		reader = csv.reader(f, delimiter=',')
		#print"----------p--------====-partner_file------",self.partner_file
		headers = {}
		for row in reader:
			col_count = 0
			for col in row:
				headers[col] = col_count
				col_count = col_count + 1
			break;
		count = 1
		for row in reader:
			print"=============2222222222===================",row[headers['CUSTOMER']]
			count = count + 1
			partner_vals = {}

			partner_vals['user_id'] = ''
			if row[headers['salesperson']]:
				salesperson = row[headers['salesperson']].strip()
				salesperson_ids = user_pool.search([('name','=',salesperson)])
				if salesperson_ids:
					salesperson_id = salesperson_ids[0]

				partner_vals['user_id'] = salesperson_ids.id

			print"==========Partner======Created==============",partner_vals
			partner_exists = partner_pool.search([('name','=',row[headers['CUSTOMER']].strip())])
			if not partner_exists:
				partner_id = partner_pool.create(partner_vals)
				print"==========Partner======Created=============="
			else:				
				partner_exists.write({'user_id': partner_vals['user_id']})				

import_customers()
