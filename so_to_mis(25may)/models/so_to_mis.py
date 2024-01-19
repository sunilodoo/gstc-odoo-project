# -*- coding: utf-8 -*-
from odoo import models, fields, osv, api, _
from odoo.tools.translate import _
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import Warning
from datetime import timedelta
import datetime

class SaleOrder(models.Model):
	_inherit = 'sale.order'

	mis_flag = fields.Boolean('Mis Flag')
	priority = fields.Char('Priority')
	sequence = fields.Char('Priority')
	dil_date = fields.Date('Delivery Date')
	payment_detail = fields.Text('Payment Details')

	@api.multi
	def update_carton_val(self):
		cartons = 0
		cbm = 0
		total_nwt_crtn = 0
		total_gwt_crtn = 0
		total_vol_wt = 0
		purchase_id = False
		vendor_id = False
		dlvy_confm_date = False
		act_dlvy_date = False
		remarks = False
		po_id = self.env['purchase.order'].search([('origin', 'like', self.name)])
		for line in self.order_line:
			edd = ''
			if line.product_uom_qty >= 1 and line.product_id.toal_qty_carton:
				cartons = float(line.product_uom_qty)/float(line.product_id.toal_qty_carton)
				cbm = (float(line.product_id.x_attr)*float(line.product_id.y_attr)*float(line.product_id.z_attr)*float(cartons))/1000000
				print"-----------prod.x_attr-------value------check--",line.product_uom_qty,line.product_id.toal_qty_carton
				total_nwt_crtn = float(cartons) * float(line.product_id.carton_nwt)
				total_gwt_crtn = float(cartons) * float(line.product_id.carton_gwt)
				total_vol_wt = float(cbm)*167
			for po in po_id:
				for p_line in po.order_line:
					if line.product_id == p_line.product_id:
						purchase_id = po.id
						vendor_id = po.partner_id.id	
					if (line.product_id == p_line.product_id) and (po.dlvy_confm_date):
						dlvy_confm_date = po.dlvy_confm_date
					if (line.product_id == p_line.product_id) and po.act_dlvy_date:
						act_dlvy_date = po.act_dlvy_date
					if (line.product_id == p_line.product_id) and po.problem:
						remarks = po.problem
					if (line.product_id == p_line.product_id) and (po.date_order and po.dlvy_confm_date):
						print"====================111111111111111"
						date1 = datetime.datetime.strptime(po.dlvy_confm_date, '%Y-%m-%d') - datetime.datetime.strptime(po.date_order, '%Y-%m-%d %H:%M:%S')
						edd = date1.days
			line.write({'cartons': float(cartons), 'vol_wt': line.product_id.vol_wt, 'cbm': float(cbm), 'total_nwt_crtn': float(total_nwt_crtn), 'total_gwt_crtn': float(total_gwt_crtn), 'total_vol_wt': float(total_vol_wt), 'purchase_id': purchase_id, 'vendor_id': vendor_id, 'edrg': dlvy_confm_date, 'adrg': act_dlvy_date, 'remarks': remarks,'edd': edd,})

	#@api.depends('target','execute')
	def update_mis(self):
		print"---------====---------=-----",self.user_id
		if not self.user_id:
			raise Warning(_("Coordinator not defined! "))
		emp = self.env['hr.employee'].search([('name','=',self.user_id.name)])
		if not emp:
			raise Warning(_("Employee not found! "))
				
		vals = {}
		vals2 = {}
		vals3 = {}
		vals4 = {}
		vals = {
				'name': emp.id,
				'order_id': self.id,
				'buyer': self.partner_id.id,
				'country': self.partner_id.country_id.id,
				'production': self.full_total,
				'target_year': 5,
				'boolen_finance': True,
			}
		vals2 = {
				'name': emp.id,
				'po_no': self.id,
				'po_date': self.confirmation_date,
				'buyer': self.partner_id.id,
				'country': self.partner_id.country_id.id,
				'amount': self.full_total,
			}
		mis = self.env['mis.reporting'].create(vals)
		mis_po = self.env['po_mis.reporting'].create(vals2)
		po_id = self.env['purchase.order'].search([('origin', 'like', self.name)])
		print"-----------------------------",po_id
		#dp = str(datetime.datetime.strptime(self.confirmation_date, '%Y-%m-%d') - datetime.datetime.strptime(self.date_order, '%Y-%m-%d %H:%M:%S')).split(',')[0].split(' ')[0]
		dp = datetime.datetime.strptime(self.confirmation_date, '%Y-%m-%d') - datetime.datetime.strptime(self.date_order, '%Y-%m-%d %H:%M:%S')
		for po in po_id:
			for line in po.order_line:
				print"----------po-----------[[[[[[[====",line,dp
				vals3 = {
					'product_id': line.product_id.id,
					'name': line.product_id.name,
					'vendor': line.order_id.partner_id.id,
					'so_id': self.id,
					'so_date': self.confirmation_date,
					'po_id': line.order_id.id,
					'state': line.order_id.state,
					'status': 'draft',
					'so_priority': self.priority,
					'po_place_date': line.order_id.date_order,
					'days_to_place': dp.days
				}
				'''
				vals4 = {
					'product_id': line.product_id.id,
					'product_uom_qty': line.product_qty,
					'product_uom': line.product_uom.id,
					'unit_price': line.price_unit,
					'price_subtotal': line.product_qty * line.price_unit,
					'pf_chrg': 0.0,
					'name': line.product_id.name,
					'vendor': line.order_id.partner_id.id,
					'po_id': line.order_id.id,
					'state': line.order_id.state,
					'po_place_date': line.order_id.date_order,
				}
				'''
				summary_mkt = self.env['po_item.history'].create(vals3)
				#summary_po = self.env['po_item.history2'].create(vals4)
		for po1 in po_id:
			for line1 in po1.order_line:
				print"----------po-----------[[[[[[[====",line1
				vals4 = {
					'product_id': line1.product_id.id,
					'product_uom_qty': line1.product_qty,
					'product_uom': line1.product_uom.id,
					'unit_price': line1.price_unit,
					'price_subtotal': line1.product_qty * line.price_unit,
					'pf_chrg': 0.0,
					'name': line1.product_id.name,
					'vendor': line1.order_id.partner_id.id,
					'so_id': self.id,
					'so_date': self.confirmation_date,
					'po_id': line1.order_id.id,
					'state': line1.order_id.state,
					'status': 'draft',
					'so_priority': self.priority,
					'po_place_date': line1.order_id.date_order,
					'days_to_place': dp.days
				}
				summary_po = self.env['po_item.history2'].create(vals4)
		self.mis_flag = True

	@api.onchange('full_total','amount_total')
	def onchange_mis(self):
		mis = self.env['mis.reporting'].search([('order_id.name','=',self.name)])
		mis_po = self.env['po_mis.reporting'].search([('po_no.name','=',self.name)])
		print"---------==mis==---------=-----",mis,self.browse(self.name),self.name
		if mis:
			mis.write({'production': self.full_total})
			mis_po.write({'amount': self.full_total})
			print"--mis---mis--------mis=====0000000000000000",mis.production

	@api.onchange('sequence')
	def change_priority(self):
		summary_mkt = self.env['po_item.history'].search([('so_id.name','=',self.name)])
		summary_po = self.env['po_item.history2'].search([('so_id.name','=',self.name)])
		print"------------change_priority------",summary_mkt,self.id,summary_po
		for mkt in summary_mkt:
			mkt.write({'so_priority': self.sequence,})
		for po in summary_po:
			po.write({'so_priority': self.sequence,})

	@api.multi
	def action_confirm(self):
		return_value = super(SaleOrder, self).action_confirm()
		for follower in self['message_follower_ids']:
			print"-------------follower----------",follower
			if follower and follower.partner_id.name != 'Administrator':
				follower.unlink()
		return return_value

	@api.depends('state', 'order_line.invoice_status')
	def _get_invoiced(self):
		"""
		Compute the invoice status of a SO. Possible statuses:
		- no: if the SO is not in status 'sale' or 'done', we consider that there is nothing to
		invoice. This is also hte default value if the conditions of no other status is met.
		- to invoice: if any SO line is 'to invoice', the whole SO is 'to invoice'
		- invoiced: if all SO lines are invoiced, the SO is invoiced.
		- upselling: if all SO lines are invoiced or upselling, the status is upselling.

		The invoice_ids are obtained thanks to the invoice lines of the SO lines, and we also search
		for possible refunds created directly from existing invoices. This is necessary since such a
		refund is not directly linked to the SO.
		"""
		summary_mkt = self.env['po_item.history'].search([('so_id.name','=',self.name)])
		summary_po = self.env['po_item.history2'].search([('so_id.name','=',self.name)])

		for order in self:
			invoice_ids = order.order_line.mapped('invoice_lines').mapped('invoice_id').filtered(lambda r: r.type in ['out_invoice', 'out_refund'])
			# Search for invoices which have been 'cancelled' (filter_refund = 'modify' in
			# 'account.invoice.refund')
			# use like as origin may contains multiple references (e.g. 'SO01, SO02')
			refunds = invoice_ids.search([('origin', 'like', order.name)]).filtered(lambda r: r.type in ['out_invoice', 'out_refund'])
			invoice_ids |= refunds.filtered(lambda r: order.name in [origin.strip() for origin in r.origin.split(',')])
			# Search for refunds as well
			refund_ids = self.env['account.invoice'].browse()
			if invoice_ids:
				for inv in invoice_ids:
					refund_ids += refund_ids.search([('type', '=', 'out_refund'), ('origin', '=', inv.number), ('origin', '!=', False), ('journal_id', '=', inv.journal_id.id)])

			# Ignore the status of the deposit product
			deposit_product_id = self.env['sale.advance.payment.inv']._default_product_id()
			line_invoice_status = [line.invoice_status for line in order.order_line if line.product_id != deposit_product_id]

			if order.state not in ('sale', 'done'):
				invoice_status = 'no'
			elif any(invoice_status == 'to invoice' for invoice_status in line_invoice_status):
				invoice_status = 'to invoice'
			elif all(invoice_status == 'invoiced' for invoice_status in line_invoice_status):
				invoice_status = 'invoiced'
			elif all(invoice_status in ['invoiced', 'upselling'] for invoice_status in line_invoice_status):
				invoice_status = 'upselling'
			else:
				invoice_status = 'no'

			if order.state == 'cancel':
				for mkt in summary_mkt:
					mkt.write({'status':'cancel',})
				for po in summary_po:
					po.write({'status':'cancel'})
			if order.state == 'sale':
				for mkt in summary_mkt:
					mkt.write({'status':'open',})
				for po in summary_po:
					po.write({'status':'open'})
			if order.state == 'done':
				for mkt in summary_mkt:
					mkt.write({'status':'done',})
				for po in summary_po:
					po.write({'status':'done'})

			order.update({
				'invoice_count': len(set(invoice_ids.ids + refund_ids.ids)),
				'invoice_ids': invoice_ids.ids + refund_ids.ids,
				'invoice_status': invoice_status
			})

class PurchaseOrder(models.Model):
	_inherit = "purchase.order"
	_order = "name desc"

	active = fields.Boolean(
        'Active', default=True,
        help="If unchecked, it will allow you to hide the PO without removing it.")
	is_notes = fields.Boolean('Is Notes?')
	Addi_info = fields.Text('Additional Info')
	dlvy_confm_date = fields.Date('DLVY Confirm date')
	dlvy_req_date = fields.Date('DLVY req. Date')
	oe_dlvy_req_date = fields.Date('Original EXP DLVY date')
	cur_dlvy_date = fields.Date('Current DLVY date')
	act_dlvy_date = fields.Date('Actual DLVY date')
	inv_date = fields.Date('Invoice date')
	bill_no = fields.Char('Bill No')
	bill_date = fields.Date('Bill date')
	sob_date = fields.Date('SOB date')
	doc_bank_date = fields.Date('Docs to bank date')
	pack_docs_day = fields.Date('Packing & docs days')
	days_dispatch = fields.Integer('Days to Dispatch')
	is_problem = fields.Boolean('is problem?', default=False)
	problem = fields.Text('Problems')
	hss = fields.Boolean('is HSS?', default=False)
	is_merger = fields.Boolean('No Need to Merge', default=False)
	priority = fields.Char('Priority')
	proc_name = fields.Many2one('hr.employee', string='Procu. Coordinator')

	days_to_place = fields.Float(string='Days to place', readonly=True)
	behind_ahead = fields.Float(string='Behind/Ahead', readonly=True)
	other_ref = fields.Char('Order Reference')
	#d_to_d = fields.Float(string='D2D', readonly=True)
	new_add = fields.Many2one('res.partner', string='New Shipping Addr.')
	new_add_bool = fields.Boolean( string='ADD Shipping Addr.')

	@api.model
	def create(self, vals):
		print"----------vals---vals-customize---",vals
		if vals.get('name', 'New') == 'New':
			vals['name'] = self.env['ir.sequence'].next_by_code('purchase.order') or '/'
		#vals['is_merger'] = True
		return super(PurchaseOrder, self).create(vals)


	@api.onchange('partner_id')
	def change_summary(self):
		summary_mkt = self.env['po_item.history'].search([('po_id.name','=',self.name)])
		summary_po = self.env['po_item.history2'].search([('po_id.name','=',self.name)])
		print"------------summary_mkt---------------",summary_mkt,self.partner_id,self.state
		for mkt in summary_mkt:
			mkt.write({'vendor': self.partner_id.id, 'state':self.state})
		for po in summary_po:
			po.write({'vendor': self.partner_id.id, 'state':self.state})

	@api.depends('state', 'order_line.qty_invoiced', 'order_line.qty_received', 'order_line.product_qty')
	def _get_invoiced(self):
		print"-------------state-------state-----------"
		summary_mkt = self.env['po_item.history'].search([('po_id.name','=',self.name)])
		summary_po = self.env['po_item.history2'].search([('po_id.name','=',self.name)])
		print"------------summary_mkt---------------",summary_mkt,self.partner_id,self.state
		for mkt in summary_mkt:
			mkt.write({'state':self.state,})
		for po in summary_po:
			po.write({'state':self.state})
		precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
		for order in self:
			if order.state not in ('purchase', 'done'):
				order.invoice_status = 'no'
				continue
			if order.state == 'cancel':
				for mkt in summary_mkt:
					mkt.write({'status':'cancel',})
				for po in summary_po:
					po.write({'status':'cancel'})
			if order.state == 'purchase':
				for mkt in summary_mkt:
					mkt.write({'status':'open',})
				for po in summary_po:
					po.write({'status':'open'})
			if order.state == 'done':
				for mkt in summary_mkt:
					mkt.write({'status':'done',})
				for po in summary_po:
					po.write({'status':'done'})

			if any(float_compare(line.qty_invoiced, line.product_qty if line.product_id.purchase_method == 'purchase' else line.qty_received, precision_digits=precision) == -1 for line in order.order_line):
				order.invoice_status = 'to invoice'
			elif all(float_compare(line.qty_invoiced, line.product_qty if line.product_id.purchase_method == 'purchase' else line.qty_received, precision_digits=precision) >= 0 for line in order.order_line) and order.invoice_ids:
				order.invoice_status = 'invoiced'
			else:
				order.invoice_status = 'no'

	@api.onchange('order_line')
	def change_line(self):
		#summary_mkt = self.env['po_item.history'].search([('po_id.name','=',self.name)])
		if self.origin:
			so = self.env['sale.order'].search([('name','ilike',self.origin[:5])])
		#print"------------Change-----line----------",self.order_line,so,self.origin
		for line in self.order_line:
			#print"--------line=======product==so==",line.product_id,line.name,line.order_id.name,so
			summary_po = self.env['po_item.history2'].search([('po_id.name','=',line.order_id.name),('product_id','=',line.product_id.id)])
			summary_mkt = self.env['po_item.history'].search([('po_id.name','=',line.order_id.name),('product_id','=',line.product_id.id)])
			for sl in so.order_line:
				print"-----------------sl------sl------",sl.product_id
				if sl.product_id.id == line.product_id.id:
					dif_vl = sl.product_uom_qty - line.product_qty
					summary_mkt.write({'name': line.name, 'dlvy_req_date': self.date_order, 'qty_not_placed': dif_vl})
					print"888888888888dif_vl888888888888888",sl.product_uom_qty,line.product_qty,dif_vl
				else:
					summary_mkt.write({'name': line.name, 'dlvy_req_date': self.date_order,})
			#for mkt in summary_mkt:
			#	mkt_prod = mkt.search([('product_id','=',line.product_id.id),('po_id.name','=',line.order_id.name)])
			print"$$$$$$$$$$$$$$$$$$$$$",summary_mkt
			summary_po.write({'name': line.name, 'product_uom_qty': line.product_qty, 'unit_price': line.price_unit, 'dlvy_req_date': self.date_order})
			



	@api.onchange('oe_dlvy_req_date')
	def change_date(self):
		print"--------------======-------",self.oe_dlvy_req_date,self.date_order
		summary_mkt = self.env['po_item.history'].search([('po_id.name','=',self.name)])
		summary_po = self.env['po_item.history2'].search([('po_id.name','=',self.name)])
		so = self.env['sale.order'].search([('name','ilike',self.origin[:5])])
		if self.oe_dlvy_req_date :
			self.pack_docs_day = datetime.datetime.strptime(self.oe_dlvy_req_date, '%Y-%m-%d') + datetime.timedelta(days=3)
		if so.confirmation_date and self.act_dlvy_date :
			diff = datetime.datetime.strptime(self.act_dlvy_date, '%Y-%m-%d') - datetime.datetime.strptime(so.confirmation_date, '%Y-%m-%d')
			self.days_dispatch = diff.days
		if so.confirmation_date and not self.act_dlvy_date :
			diff = datetime.datetime.strptime(self.pack_docs_day, '%Y-%m-%d') - datetime.datetime.strptime(so.confirmation_date, '%Y-%m-%d')
			self.days_dispatch = diff.days
		if self.oe_dlvy_req_date and self.cur_dlvy_date:
			diff1 = datetime.datetime.strptime(self.cur_dlvy_date, '%Y-%m-%d') - datetime.datetime.strptime(self.oe_dlvy_req_date, '%Y-%m-%d')
			self.behind_ahead = diff1.days
		for mkt in summary_mkt:
			mkt.write({'oe_dlvy_req_date': self.oe_dlvy_req_date, 'pack_docs_day': self.pack_docs_day, 'days_dispatch': self.days_dispatch, 'behind_ahead': self.behind_ahead,})
		for po in summary_po:
			po.write({'oe_dlvy_req_date': self.oe_dlvy_req_date, 'pack_docs_day': self.pack_docs_day, 'days_dispatch': self.days_dispatch, 'behind_ahead': self.behind_ahead,})
		print"------------summary_mkt-----------summary_po----",summary_mkt,summary_po


	@api.onchange('dlvy_confm_date','dlvy_req_date','cur_dlvy_date','act_dlvy_date','inv_date','bill_no','bill_date','sob_date','doc_bank_date')
	def change_valu(self):
		summary_mkt = self.env['po_item.history'].search([('po_id.name','=',self.name)])
		summary_po = self.env['po_item.history2'].search([('po_id.name','=',self.name)])
		so = self.env['sale.order'].search([('name','ilike',self.origin[:5])])
		if self.oe_dlvy_req_date and self.cur_dlvy_date:
			diff1 = datetime.datetime.strptime(self.cur_dlvy_date, '%Y-%m-%d') - datetime.datetime.strptime(self.oe_dlvy_req_date, '%Y-%m-%d')
			self.behind_ahead = diff1.days
		#if self.cur_dlvy_date and so.confirmation_date:
		#	diff2 = datetime.datetime.strptime(self.cur_dlvy_date, '%Y-%m-%d') - datetime.datetime.strptime(so.confirmation_date, '%Y-%m-%d')
		#	self.d_to_d = diff2.days
		for mkt in summary_mkt:
			mkt.write({'dlvy_confm_date': self.dlvy_confm_date, 'dlvy_req_date': self.dlvy_req_date, 'cur_dlvy_date': self.cur_dlvy_date, 'act_dlvy_date': self.act_dlvy_date, 'inv_date': self.inv_date, 'bill_no': self.bill_no, 'bill_date': self.bill_date, 'sob_date': self.sob_date, 'doc_bank_date': self.doc_bank_date, 'behind_ahead': self.behind_ahead,})
		for po in summary_po:
			po.write({'dlvy_confm_date': self.dlvy_confm_date, 'dlvy_req_date': self.dlvy_req_date, 'cur_dlvy_date': self.cur_dlvy_date, 'act_dlvy_date': self.act_dlvy_date, 'inv_date': self.inv_date, 'bill_no': self.bill_no, 'bill_date': self.bill_date, 'sob_date': self.sob_date, 'doc_bank_date': self.doc_bank_date, 'behind_ahead': self.behind_ahead, })
		print"------------summary_mkt-----------summary_po----",summary_mkt,summary_po

	@api.onchange('is_problem','problem')
	def change_problem(self):
		summary_mkt = self.env['po_item.history'].search([('po_id.name','=',self.name)])
		summary_po = self.env['po_item.history2'].search([('po_id.name','=',self.name)])
		print"------------summary_mkt---------ffffffff------",summary_mkt,self.id,summary_po
		for mkt in summary_mkt:
			mkt.write({'is_problem': self.is_problem, 'problem': self.problem,})
		for po in summary_po:
			po.write({'is_problem': self.is_problem, 'problem': self.problem, })

	@api.onchange('sequence','proc_name')
	def change_priority(self):
		summary_mkt = self.env['po_item.history'].search([('po_id.name','=',self.name)])
		summary_po = self.env['po_item.history2'].search([('po_id.name','=',self.name)])
		print"------------change_priority------",summary_mkt,self.id,summary_po
		for mkt in summary_mkt:
			mkt.write({'priority': self.sequence, 'proc_name':self.proc_name.id})
		for po in summary_po:
			po.write({'priority': self.sequence, 'proc_name': self.proc_name.id})

	@api.model
	def _prepare_picking(self):
		if not self.group_id:
			self.group_id = self.group_id.create({
				'name': self.name,
				'partner_id': self.partner_id.id
			})
		if self.origin and 'SO' in self.origin:
			so = self.env['sale.order'].search([('name','ilike',self.origin[:5])])
			so_id = so.id
		else:
			so_id = False
		if self.hss == True:
			pick = self.env['stock.picking.type'].search([('name','=','HSS')])
			pick_id = pick.id
		else:
			pick_id = self.picking_type_id.id
		if not self.partner_id.property_stock_supplier.id:
			raise UserError(_("You must set a Vendor Location for this partner %s") % self.partner_id.name)
		return {
			'picking_type_id': pick_id,
			'partner_id': self.partner_id.id,
			'date': self.date_order,
			'min_date': self.date_planned,
			'origin': self.name,
			'so_no': so_id,
			'location_dest_id': self._get_destination_location(),
			'location_id': self.partner_id.property_stock_supplier.id,
			'company_id': self.company_id.id,
		}

	@api.onchange('date_order')
	def change_order_date(self):
		print"--------------======---fffffffsssssss----",self.oe_dlvy_req_date,self.date_order
		summary_mkt = self.env['po_item.history'].search([('po_id.name','=',self.name)])
		summary_po = self.env['po_item.history2'].search([('po_id.name','=',self.name)])
		if self.origin and 'SO' in self.origin:
			so = self.env['sale.order'].search([('name','ilike',self.origin[:5])])

		if so.confirmation_date :
			d = datetime.datetime.strptime(so.confirmation_date, '%Y-%m-%d') - datetime.datetime.strptime(self.date_order, '%Y-%m-%d %H:%M:%S')
			days_to_place = d.days
		for mkt in summary_mkt:
			mkt.write({'days_to_place': days_to_place,})
		for po in summary_po:
			po.write({'days_to_place': days_to_place,})





