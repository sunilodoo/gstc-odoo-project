# -*- coding: utf-8 -*-
from odoo import models, fields, osv, api, _
from odoo.tools.translate import _
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.exceptions import Warning
from datetime import timedelta
import datetime

class CrmLead(models.Model):
	_inherit = 'crm.lead'

	# customer_type = fields.Many2one('customer.type', string="Customer Type")
	cust_type = fields.Many2one('customer.type', string="Customer Type")
	lead_image = fields.Many2many('ir.attachment', 'lead_attachments_rel',
        'lead_id', 'attachment_id', string='Attachments')
	# classification_id = fields.Many2one('customer.classify', string="Classification")
	product_interest = fields.Many2many('product.interest', string="Product of Interest", compute='_compute_product_interest_ids',  inverse='_set_product_interest')
	tagging = fields.Many2many('res.partner.category', string="Tags", compute='_compute_tagging',  inverse='_set_tagging')
	# tagging = fields.Many2many('res.partner.category', string="Tags")
	remarks = fields.Text('Remarks')
	old_customer = fields.Boolean('Old/Lost Customer')
	compt_customer = fields.Boolean('Competetor Customer')
	new_customer = fields.Boolean('New Customer')
	lead_priority = fields.Selection([('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10')], string='Priority')
	mail_sent_date = fields.Date("Mailed Date")
	reminder1_date = fields.Date("Reminder1 Date")
	reminder2_date = fields.Date("Reminder2 Date")
	reminder3_date = fields.Date("Reminder3 Date")

	@api.multi
	@api.depends('partner_id',)
	@api.onchange('partner_id')
	def _compute_product_interest_ids(self):
		for rec in self:
			rec.product_interest = rec.partner_id.product_interest
	@api.multi
	@api.depends('product_interest')
	@api.onchange('product_interest')
	def _set_product_interest(self):
		for rec in self:
			if rec.partner_id:
				rec.partner_id.product_interest = rec.product_interest

	@api.multi
	@api.depends('partner_id',)
	# @api.onchange('partner_id')
	def _compute_tagging(self):
		for rec in self:
			rec.tagging = rec.partner_id.category_id
	@api.multi
	@api.depends('tagging')
	# @api.onchange('tagging')
	def _set_tagging(self):
		for rec in self:
			if rec.partner_id:
				rec.partner_id.category_id = rec.tagging
	
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
		self.classification_id = self.partner_id.classification_id or ''
		if self.partner_id and self.partner_id.product_interest:
			self.product_interest = [(6, 0, [x.id for x in self.partner_id.product_interest])]
		if self.partner_id and self.partner_id.product_interest:
			self.tagging = [(6, 0, [categ.id for categ in self.partner_id.category_id])]
		

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

	@api.multi
	def send_intro(self):
		print"--------self------send_intro---",self
		form_view_id = self.env.ref('mail.view_mail_form')
		template=self.env["mail.template"].search([('name','=','Lead Introduction Template')])
		ctx = dict()
		ctx.update({
			'default_model': 'crm.lead',
			'default_res_id': self.ids[0],
			'default_use_template': bool(template),
			'default_template_id': template.id,
			'default_composition_mode': 'comment',
			'custom_layout': "email_tmpl_lead_intoroduction"
		})
		print"------template---",template,template.id,ctx
		#self.stage_id = 1
		return {
			'name': 'Lead Introduction Template',
			'type': 'ir.actions.act_window',
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'mail.mail',
			'views': [(form_view_id.id, 'form'), ],
			'view_id': form_view_id.id,
			'target': 'new',
			'context': ctx,
		}

	@api.multi
	def send_reminder(self):
		print"--------self------send_reminder---",self
		form_view_id = self.env.ref('mail.view_mail_form')
		template=self.env["mail.template"].search([('name','=','Lead: Reminder')])
		template.write({'email_to': 'odoo@healthgenie.in'})
		template.send_mail(222, force_send=True)

class CustomerType(models.Model):
	_name = 'customer.type'

	name = fields.Char('Name')

class LeadImage(models.Model):
	_name = 'lead.image'

	name = fields.Char('Name')
	image = fields.Binary('Image')
	l_id = fields.Many2one('crm.lead', string='Img ID')

class WizMail(models.Model):
	_inherit="mail.mail"

	template_id = fields.Many2one('mail.template','Use template',index=True,domain="[('model', '=', model)]")
	email_cc = fields.Char('CC')

	@api.multi
	@api.onchange('template_id')
	def onchange_template_id_wrapper(self):
		self.ensure_one()
		values = self.onchange_template_id(self.template_id.id,self.res_id,self.model)['value']
		for fname, value in values.iteritems():
			setattr(self, fname, value)

	@api.multi
	def onchange_template_id(self, template_id,res_id,model):
		mail_cc=''
		lead=self.env['crm.lead']
		active_id=lead._context.get('active_ids')
		record = lead.browse(active_id)
		mail_to=record.email_from
		mail_from=record.user_id.login
		reply_to=record.user_id.login
		if template_id :
			template = self.env['mail.template'].browse(template_id)
			fields = [ 'subject', 'body_html','attachment_ids']
			values = dict((field, getattr(template, field)) for field in fields if getattr(template, field))
			if template.attachment_ids:
				values['attachment_ids'] = [att.id for att in template.attachment_ids]
			if template.user_signature and 'body_html' in values:
				signature = self.env.user.signature
				values['body_html'] = tools.append_content_to_html(values['body_html'], signature, plaintext=False)
		elif template_id:
			values = self.generate_email_for_composer(template_id, [res_id])[res_id]
			# transform attachments into attachment_ids; not attached to the document because this will
			# be done further in the posting process, allowing to clean database if email not send
			Attachment = self.env['ir.attachment']
			for attach_fname, attach_datas in values.pop('attachments', []):
				data_attach = {
					'name': attach_fname,
					'datas': attach_datas,
					'datas_fname': attach_fname,
					'res_model': 'mail.mail',
					'res_id': 0,
					'type': 'binary',  # override default_type from context, possibly meant for another model!
				}
				values.setdefault('attachment_ids', list()).append(Attachment.create(data_attach).id)
		else:
			default_values = self.with_context(default_model=model, default_res_id=res_id).default_get(['model', 'res_id','email_to', 'recipient_ids', 'subject', 'body_html', 'email_from', 'reply_to', 'attachment_ids'])
			values = dict((key, default_values[key]) for key in ['subject', 'body_html', 'recipient_ids', 'email_from', 'reply_to', 'attachment_ids'] if key in default_values)

		if values.get('body_html'):
			values['body_html'] = values.pop('body_html')

		# This onchange should return command instead of ids for x2many field.
		# ORM handle the assignation of command list on new onchange (api.v8),
		# this force the complete replacement of x2many field with
		# command and is compatible with onchange api.v7
		values = self._convert_to_write(values)
		print'------------------values--------mail_cc--',self._uid,mail_cc
		lead_id = self.env['crm.lead'].search([('id','=',res_id)])
		if lead_id and lead_id.contact_name:
			values['body_html'] = values['body_html'].replace("Dear ${object.contact_name or 'Sir/Madam'}", 'Dear '+str(lead_id.contact_name))
		else:
			values['body_html'] = values['body_html'].replace("Dear ${object.contact_name or 'Sir/Madam'}", 'Dear Sir/Madam')

		login_user = self.env['res.users'].search([('id','=',self._uid)])

		values['email_to'] = 'odoo@healthgenie.in'
		values['email_from'] = 'gstc@gstc.com'
		#values['email_cc'] = login_user.email or ''
		#values['reply_to'] = login_user.email
		lead_id.write({'stage_id': 1, 'mail_sent_date': datetime.datetime.now().date()})
		return {'value':values}
