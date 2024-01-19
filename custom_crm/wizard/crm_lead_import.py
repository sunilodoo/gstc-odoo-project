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


class CrmLeadImport(models.TransientModel):
	_name = 'crm.lead.import'
	_description = "Crm Lead Import"

	lead_file = fields.Binary(string='CSV File', help='File should be separated by comma (,) ')
	tagging_id = fields.Many2one('res.partner.category', string='Source')
	
	@api.multi
	def lead_update(self):
		partner_pool = self.env['res.partner']
		country_pool = self.env['res.country']
		state_pool = self.env['res.country.state']
		user_pool  = self.env['res.users']
		tagg_pool  = self.env['res.partner.category']
		classification_pool  = self.env['customer.classify']
		profile_pool  = self.env['company.profile']
		interest_pool  = self.env['product.interest']
		#--------------------------------------------------------------current---------------------------------------------------------------------------------
		lead_pool  = self.env['crm.lead']



		f = StringIO.StringIO(base64.decodestring(self.lead_file))
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
			# print"=============2222222222===================",row[headers['CUSTOMER']]
			count = count + 1
			#if not row[headers['CONTACT NAME']]:
			partner_vals = {
				#'old_customer': True,
				# 'customer': True,
                'email'   : row[headers['Email']].strip(),
                'street'  : row[headers['STREET 1']].strip(),
                # 'street2'  : row[headers['STREET2']].strip(),
                'city'    : row[headers['REGION']].strip(),
                'zip'     : row[headers['P CODE']].strip(),
                'phone'   : row[headers['TEL']].strip(),
                'mobile': row[headers['MOB']].strip(),
                'fax'   : row[headers['FAX']].strip(),
                #'function'   : row[headers['CONTACT POSITION']].strip(),
                'website': row[headers['Website']].strip(),
                'comment': row[headers['Remarks']].strip(),
			}
			if row[headers['Company Name']] and row[headers['Contact Person']]:
				partner_vals['name'] = row[headers['Company Name']].strip()
				partner_vals['is_company'] = True
				partner_vals['child_ids'] = [(0,0, {'name': row[headers['Contact Person']].strip()})]
			elif row[headers['Company Name']]:
				partner_vals['name'] = row[headers['Company Name']].strip()
			elif row[headers['Contact Person']]:
				partner_vals['name'] = row[headers['Contact Person']].strip()

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
			if row[headers['Country']]:
				country = row[headers['Country']].strip()
				country_ids = country_pool.search([('name','=',country.capitalize())])
				if country_ids:
					country_id = country_ids[0]
				else:
					raise Warning(_("Country not defined! "+country))
				partner_vals['country_id'] = country_id.id
				partner_vals['ref'] = country_id.code if country_id.code else country_id.name

			partner_vals['category_id'] = [(6, 0, [self.tagging_id.id])]
			# partner_vals['category_id'] = ''
			# if row[headers['Source']]:
			# 	tagging = row[headers['Source']].strip()
			# 	tagging_ids = tagg_pool.search([('name','=',tagging)])
			# 	if tagging_ids:
			# 		tagging_id = tagging_ids[0]
			# 	partner_vals['category_id'] = [(6, 0, [tagging_id.id])]

			partner_vals['classification_id'] = ''
			if row[headers['Classification']]:
				classification = row[headers['Classification']].strip()
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
			if row[headers['company profile']]:
				profile = row[headers['company profile']].strip()
				profile_ids = profile_pool.search([('name','=',profile)])
				if profile_ids:
					profile_id = profile_ids[0]
				partner_vals['company_profile'] = [(6, 0, [profile_id.id])]

			partner_vals['product_interest'] = ''
			if row[headers['product of interest']]:
				interest = row[headers['product of interest']].strip()
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


	# @api.multi
	# def update_customer(self):

	# 	partner_pool = self.env['res.partner']
	# 	user_pool  = self.env['res.users']

	# 	f = StringIO.StringIO(base64.decodestring(self.partner_file))
	# 	reader = csv.reader(f, delimiter=',')
	# 	#print"----------p--------====-partner_file------",self.partner_file
	# 	headers = {}
	# 	for row in reader:
	# 		col_count = 0
	# 		for col in row:
	# 			headers[col] = col_count
	# 			col_count = col_count + 1
	# 		break;
	# 	count = 1
	# 	for row in reader:
	# 		print"=============2222222222===================",row[headers['CUSTOMER']]
	# 		count = count + 1
	# 		partner_vals = {}

	# 		partner_vals['user_id'] = ''
	# 		if row[headers['salesperson']]:
	# 			salesperson = row[headers['salesperson']].strip()
	# 			salesperson_ids = user_pool.search([('name','=',salesperson)])
	# 			if salesperson_ids:
	# 				salesperson_id = salesperson_ids[0]

	# 			partner_vals['user_id'] = salesperson_ids.id

	# 		print"==========Partner======Created==============",partner_vals
	# 		partner_exists = partner_pool.search([('name','=',row[headers['CUSTOMER']].strip())])
	# 		if not partner_exists:
	# 			partner_id = partner_pool.create(partner_vals)
	# 			print"==========Partner======Created=============="
	# 		else:				
	# 			partner_exists.write({'user_id': partner_vals['user_id']})

	@api.multi
	def lead_create(self):
		partner_pool = self.env['res.partner']
		country_pool = self.env['res.country']
		state_pool = self.env['res.country.state']
		user_pool  = self.env['res.users']
		tagg_pool  = self.env['res.partner.category']
		classification_pool  = self.env['customer.classify']
		profile_pool  = self.env['company.profile']
		interest_pool  = self.env['product.interest']
		#--------------------------------------------------------------current---------------------------------------------------------------------------------
		lead_pool  = self.env['crm.lead']
		f = StringIO.StringIO(base64.decodestring(self.lead_file))
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
			count = count + 1
			lead_vals = {
                'name'   : row[headers['Opportunity']].strip(),
                'title_action'   : row[headers['Title Action']].strip(),
                'date_deadline'   : row[headers['Expected Closing']].strip(),
			}
			partner_vals = {
                'name':row[headers['Company']].strip(),
                'company_type':'company',
                'email'   : row[headers['Email']].strip(),
                'mobile': row[headers['Mobile']].strip(),
                'phone'   : row[headers['Phone']].strip(),
			}
			country= row[headers['Country']].strip()
			if country:
				country_ids = country_pool.search([('name','=',country.title())])
				if country_ids:
					country_id = country_ids[0]
				else:
					raise Warning(_("Country not defined! as "+country+' in line '+str(count)))
				partner_vals['country_id'] = country_id.id
			source= row[headers['Source']].strip()
			if source:
				source_id = self.env['utm.source'].search([('name','=',source)])
				if source_id:
					lead_vals['source_id'] = source_id[0].id
				else:
					raise Warning(_("Source not defined! as "+source+' in line '+str(count)))

			medium= row[headers['Medium']].strip()
			if medium:
				medium_id = self.env['utm.medium'].search([('name','=',medium)])
				if medium_id:
					lead_vals['medium_id'] = medium_id[0].id
				else:
					raise Warning(_("Medium not defined! as "+medium+' in line '+str(count)))

			tags= row[headers['Tags']].strip()
			if tags:
				tags_id = self.env['res.partner.category'].search([('name','=',tags)])
				if tags_id:
					partner_vals['category_id'] = [(6, 0, [tags_id.id])]
					# lead_vals['tagging'] = [(6, 0, [tags_id.id])]
				else:
					raise Warning(_("Tags not defined! as "+tags+' in line '+str(count)))

			lead= row[headers['Leads']].strip()
			if lead:
				lead_id = self.env['custom.lead'].search([('name','=',lead)])
				if lead_id:
					lead_vals['lead'] = lead_id[0].id
				else:
					raise Warning(_("Leads not defined! as "+lead+' in line '+str(count)))

			pi= row[headers['Product of Interest']].strip()
			if pi:
				pi_id = self.env['product.interest'].search([('name','=',pi)])
				if pi_id:
					partner_vals['product_interest'] = [(6, 0, [pi_id.id])]
				else:
					raise Warning(_("Product of Interest is not defined! as "+pi+' in line '+str(count)))\

			sales_team= row[headers['Sales Team']].strip()
			if sales_team:
				sales_team_id = self.env['crm.team'].search([('name','=',sales_team)])
				if sales_team_id:
					lead_vals['team_id'] = sales_team_id[0].id
				else:
					raise Warning(_("Sales Team not defined! as "+sales_team+' in line '+str(count)))

			next_activity= row[headers['Next Activity']].strip()
			if next_activity:
				next_activity_id = self.env['crm.activity'].search([('name','=',next_activity)])
				if next_activity_id:
					lead_vals['next_activity_id'] = next_activity_id[0].id
				else:
					raise Warning(_("Next Activity not defined! as "+next_activity+' in line '+str(count)))

			date_action= row[headers['Action Date']].strip()
			if date_action:
				d_a = datetime.strptime(date_action, "%d-%m-%Y %H:%M:%S")
				lead_vals['date_action'] = d_a.date()

			user= row[headers['Sales Person']].strip()
			if user:
				user_id = self.env['res.users'].search([('name','=',user)])
				if user_id:
					lead_vals['user_id'] = user_id[0].id
				else:
					raise Warning(_("Sales Person not defined! as "+user+' in line '+str(count)))

			customer_type= row[headers['Customer Type']].strip()
			if customer_type:
				customer_type_id = self.env['customer.type'].search([('name','=',customer_type)])
				if customer_type_id:
					lead_vals['cust_type'] = customer_type_id[0].id
				else:
					raise Warning(_("Customer Type not defined! as "+customer_type+' in line '+str(count)))

			visitor_no= row[headers['Visitor No']].strip()
			if visitor_no:
				lead_vals['visitor_no'] = visitor_no
			visitor_date= row[headers['Visitor Date']].strip()
			if visitor_date:
				lead_vals['visit_date'] = datetime.strptime(visitor_date, "%d-%m-%Y %H:%M:%S").date()

			classification= row[headers['Classification & Priority']].strip()
			if classification:
				customer_classification_id = self.env['customer.classify'].search([('name','=',classification)])
				if customer_classification_id:
					lead_vals['classification_id'] = customer_classification_id[0].id
				else:
					raise Warning(_("Classification & Priority not defined! as "+classification+' in line '+str(count)))

			targat_value= row[headers['Target Value']].strip()
			if targat_value:
				targat_value_id = self.env['targat.value'].search([('name','=',targat_value)])
				if targat_value_id:
					lead_vals['targat_value'] = targat_value_id[0].id
				else:
					lead_vals['targat_value'] = self.env['targat.value'].create({'name': targat_value})
			rating= row[headers['Rating']].strip()
			if rating:
				lead_vals['priority'] = rating
			day_assign= row[headers['Days to Assign']].strip()
			if day_assign:
				lead_vals['day_open'] = day_assign
			day_close= row[headers['Days to Close']].strip()
			if day_close:
				lead_vals['day_close'] = day_close
			potential_value= row[headers['Potential value']].strip()
			if potential_value:
				lead_vals['referred'] = potential_value
			r_f_n_c= row[headers['Reason for Non Closure']].strip()
			if r_f_n_c:
				lead_vals['reason_for_n_closure'] = r_f_n_c
			description= row[headers['Description']].strip()
			if description:
				lead_vals['description'] = description
		f.seek(0)
		headers = {}
		for row in reader:
			col_count = 0
			for col in row:
				headers[col] = col_count
				col_count = col_count + 1
			break;
		count =2
		previous_company = ''
		previous_lead_id = ''
		for row in reader:
			count = count + 1
			lead_vals = {
                'name'   : row[headers['Opportunity']].strip(),
                'title_action'   : row[headers['Title Action']].strip(),
                'date_deadline'   : row[headers['Expected Closing']].strip(),
			}
			partner_vals = {
                'name':row[headers['Company']].strip(),
                'company_type':'company',
                'email'   : row[headers['Email']].strip(),
                'mobile': row[headers['Mobile']].strip(),
                'phone'   : row[headers['Phone']].strip(),
			}
			country= row[headers['Country']].strip()
			if country:
				country_ids = country_pool.search([('name','=',country.title())])
				if country_ids:
					country_id = country_ids[0]
				else:
					raise Warning(_("Country not defined! as "+country+' in line '+str(count)))
				partner_vals['country_id'] = country_id.id
			source= row[headers['Source']].strip()
			if source:
				source_id = self.env['utm.source'].search([('name','=',source)])
				if source_id:
					lead_vals['source_id'] = source_id[0].id
				else:
					raise Warning(_("Source not defined! as "+source+' in line '+str(count)))

			medium= row[headers['Medium']].strip()
			if medium:
				medium_id = self.env['utm.medium'].search([('name','=',medium)])
				if medium_id:
					lead_vals['medium_id'] = medium_id[0].id
				else:
					raise Warning(_("Medium not defined! as "+medium+' in line '+str(count)))

			tags= row[headers['Tags']].strip()
			if tags:
				tags_id = self.env['res.partner.category'].search([('name','=',tags)])
				if tags_id:
					partner_vals['category_id'] = [(6, 0, [tags_id.id])]
					# lead_vals['tagging'] = [(6, 0, [tags_id.id])]
				else:
					raise Warning(_("Tags not defined! as "+tags+' in line '+str(count)))

			lead= row[headers['Leads']].strip()
			if lead:
				lead_id = self.env['custom.lead'].search([('name','=',lead)])
				if lead_id:
					lead_vals['lead'] = lead_id[0].id
				else:
					raise Warning(_("Leads not defined! as "+lead+' in line '+str(count)))

			pi= row[headers['Product of Interest']].strip()
			if pi:
				pi_id = self.env['product.interest'].search([('name','=',pi)])
				if pi_id:
					partner_vals['product_interest'] = [(6, 0, [pi_id.id])]
				else:
					raise Warning(_("Product of Interest is not defined! as "+pi+' in line '+str(count)))\

			sales_team= row[headers['Sales Team']].strip()
			if sales_team:
				sales_team_id = self.env['crm.team'].search([('name','=',sales_team)])
				if sales_team_id:
					lead_vals['team_id'] = sales_team_id[0].id
				else:
					raise Warning(_("Sales Team not defined! as "+sales_team+' in line '+str(count)))

			next_activity= row[headers['Next Activity']].strip()
			if next_activity:
				next_activity_id = self.env['crm.activity'].search([('name','=',next_activity)])
				if next_activity_id:
					lead_vals['next_activity_id'] = next_activity_id[0].id
				else:
					raise Warning(_("Next Activity not defined! as "+next_activity+' in line '+str(count)))

			date_action= row[headers['Action Date']].strip()
			if date_action:
				d_a = datetime.strptime(date_action, "%d-%m-%Y %H:%M:%S")
				lead_vals['date_action'] = d_a.date()

			user= row[headers['Sales Person']].strip()
			if user:
				user_id = self.env['res.users'].search([('name','=',user)])
				if user_id:
					lead_vals['user_id'] = user_id[0].id
				else:
					raise Warning(_("Sales Person not defined! as "+user+' in line '+str(count)))

			customer_type= row[headers['Customer Type']].strip()
			if customer_type:
				customer_type_id = self.env['customer.type'].search([('name','=',customer_type)])
				if customer_type_id:
					lead_vals['cust_type'] = customer_type_id[0].id
				else:
					raise Warning(_("Customer Type not defined! as "+customer_type+' in line '+str(count)))

			visitor_no= row[headers['Visitor No']].strip()
			if visitor_no:
				lead_vals['visitor_no'] = visitor_no
			visitor_date= row[headers['Visitor Date']].strip()
			if visitor_date:
				lead_vals['visit_date'] = datetime.strptime(visitor_date, "%d-%m-%Y %H:%M:%S").date()

			classification= row[headers['Classification & Priority']].strip()
			if classification:
				customer_classification_id = self.env['customer.classify'].search([('name','=',classification)])
				if customer_classification_id:
					lead_vals['classification_id'] = customer_classification_id[0].id
				else:
					raise Warning(_("Classification & Priority not defined! as "+classification+' in line '+str(count)))

			targat_value= row[headers['Target Value']].strip()
			if targat_value:
				targat_value_id = self.env['targat.value'].search([('name','=',targat_value)])
				if targat_value_id:
					lead_vals['targat_value'] = targat_value_id[0].id
				else:
					lead_vals['targat_value'] = self.env['targat.value'].create({'name': targat_value})
			rating= row[headers['Rating']].strip()
			if rating:
				lead_vals['priority'] = rating
			day_assign= row[headers['Days to Assign']].strip()
			if day_assign:
				lead_vals['day_open'] = day_assign
			day_close= row[headers['Days to Close']].strip()
			if day_close:
				lead_vals['day_close'] = day_close
			potential_value= row[headers['Potential value']].strip()
			if potential_value:
				lead_vals['referred'] = potential_value
			r_f_n_c= row[headers['Reason for Non Closure']].strip()
			if r_f_n_c:
				lead_vals['reason_for_n_closure'] = r_f_n_c
			description= row[headers['Description']].strip()
			if description:
				lead_vals['description'] = description
			current_company= row[headers['Company']].strip()
			if previous_company == current_company:
				child_vals={
					'name': row[headers['Contact Person']].strip(),
					'company_type':'person',
					'email': row[headers['Email']].strip(),
					'mobile': row[headers['Mobile']].strip(),
				}
				val = {'child_ids': [(0,0, child_vals)]}
				previous_lead_id.partner_id.write(val)
			elif not current_company:
				child_vals={
					'name': row[headers['Contact Person']].strip(),
					'company_type':'person',
					'email': row[headers['Email']].strip(),
					'mobile': row[headers['Mobile']].strip(),
				}
				val = {'child_ids': [(0,0, child_vals)]}
				previous_lead_id.partner_id.write(val)
			else:
				child_vals={
					'name': row[headers['Contact Person']].strip(),
					'email': row[headers['Email']].strip(),
					'mobile': row[headers['Mobile']].strip(),
				}
				partner_vals['child_ids'] = [(0,0, child_vals)]
				partner_id = partner_pool.create(partner_vals)
				partner_id.onchange_company_type()
				lead_vals['partner_id'] = partner_id.id
				previous_lead_id = self.env['crm.lead'].create(lead_vals)
				previous_lead_id._onchange_partner_id()
				previous_lead_id._onchange_user_id()
				previous_lead_id._onchange_next_activity_id()
				previous_company= current_company