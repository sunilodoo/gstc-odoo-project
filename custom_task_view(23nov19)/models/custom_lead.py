# -*- coding: utf-8 -*-
from odoo import models, fields, osv, api, _
from odoo.tools.translate import _
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.exceptions import Warning
from datetime import timedelta
import datetime

class CrmLead(models.Model):
	_inherit = 'crm.lead'

	cust_type = fields.Many2one('customer.type', string="Customer Type")
	lead_image = fields.One2many('lead.image','l_id',string="Image")
	remarks = fields.Text('Remarks')
	old_customer = fields.Boolean('Old/Lost Customer')
	compt_customer = fields.Boolean('Competetor Customer')
	new_customer = fields.Boolean('New Customer')
	
	@api.onchange('partner_id')
	def change_partners(self):
		print"----change--partner----",self.partner_id
		self.email_from = self.partner_id.email
		self.phone = self.partner_id.phone
		self.user_id = self.partner_id.user_id.id
		self.partner_name = self.partner_id.name
		self.street = self.partner_id.street
		self.street2 = self.partner_id.street2
		self.city = self.partner_id.city
		self.state_id = self.partner_id.state_id.id
		self.country_id = self.partner_id.country_id.id
		self.zip = self.partner_id.zip
		self.mobile = self.partner_id.mobile
		self.fax = self.partner_id.fax

	def add_on_calendar(self):
		print"-----addon---calendar--",self,self.next_activity_id,self.next_activity_id.name,self.date_action,self.title_action
		meeting = self.env['calendar.event'].search([('name','=',self.next_activity_id.name)])
		values = {}
		if self.next_activity_id and self.date_action and self.title_action:
		#print"---------vrrrrrrrrrrrrrrrrrrrrr-------",meeting
		    values = {  'name': self.title_action,
		                'start_datetime': self.date_action,
		                'stop_datetime': self.date_deadline,
		                'opportunity_id':self.id,
		                'start': self.date_action,
		                'stop': self.date_deadline,
		                'partner_ids': [(6, 0, [])],
		    }
		    meeting = self.env['calendar.event'].create(values)

	'''
	@api.onchange('old_customer','compt_customer','new_customer')
	def change_type(self):
		print"----------",self.partner_id
		res = self.env['res.partner'].search([('id','=',self.partner_id.id)])
		if (self.partner_id) and (self.old_customer == True):
			res.write({'old_cust': True})
		else:
			res.write({'old_cust': False})
		if (self.partner_id) and (self.compt_customer == True):
			res.write({'compt_cust': True})
		else:
			res.write({'compt_cust': False})
		if (self.partner_id) and (self.new_customer == True):
			res.write({'new_cust': True})
		else:
			res.write({'new_cust': False})

	@api.onchange('referred')
	def change_potential(self):
		print"----------",self.partner_id,self.referred
		res = self.env['res.partner'].search([('id','=',self.partner_id.id)])
		if (self.partner_id) and (self.referred):
			res.write({'potvl': self.referred})
	'''

class CustomerType(models.Model):
	_name = 'customer.type'

	name = fields.Char('Name')

class LeadImage(models.Model):
	_name = 'lead.image'

	name = fields.Char('Name')
	image = fields.Binary('Image')
	l_id = fields.Many2one('crm.lead', string='Img ID')
