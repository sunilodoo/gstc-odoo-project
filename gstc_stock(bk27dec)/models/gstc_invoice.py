# -*- coding: utf-8 -*-

from odoo import models, fields, osv, api, _
from odoo.tools.translate import _
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import Warning
from datetime import timedelta
import datetime

class AccountInvoice(models.Model):
	_inherit = "account.invoice"

	is_consignee = fields.Boolean('Inv to consignee')
	consignee = fields.Many2one('res.partner', string='Consignee')
	hide_dispatch=fields.Boolean('Hide',default=False)

	@api.multi
	@api.model
	def dispatch(self):
		dis=True
		origin=self.origin
		if origin and ('SO' in origin):
			order=self.env['sale.order'].search([('name','=like',origin)],limit=1)
			purchase_orders=self.env['purchase.order'].search([('origin','like',origin)])
			for po in purchase_orders:
				if po.picking_ids:
					for pick in po.picking_ids:
						if (pick.state != 'done'): 
							dis=False
							break
					if not dis:
						break
				else:
					raise UserError(_("Purchase Order Not Confirmed"))
		
			if dis:
				if order:
					for picks in order.picking_ids:
						if picks.state not in ['draft','cancel','done']:
							picks.force_assign()
							wiz = self.env['stock.immediate.transfer'].create({'pick_id': picks.id})
							wiz.process()
							self.hide_dispatch=True
						else:
							raise UserError(_("Stock already Dispatched"))
			else:
				raise UserError(_("Shipment not Received yet!!!"))
		return
	





