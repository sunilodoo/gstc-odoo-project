# -*- coding: utf-8 -*-

from odoo import models, fields, osv, api, _
from odoo.tools.translate import _
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import Warning
from datetime import timedelta
import datetime

class ProcurementOrder(models.Model):
	_inherit = "procurement.order"


	@api.multi
	def _prepare_purchase_order_line(self, po, supplier):
		self.ensure_one()

		procurement_uom_po_qty = self.product_uom._compute_quantity(self.product_qty, self.product_id.uom_po_id)
		seller = self.product_id._select_seller(
			partner_id=supplier.name,
			quantity=procurement_uom_po_qty,
			date=po.date_order and po.date_order[:10],
			uom_id=self.product_id.uom_po_id)

		taxes = self.product_id.supplier_taxes_id
		fpos = po.fiscal_position_id
		taxes_id = fpos.map_tax(taxes) if fpos else taxes
		if taxes_id:
			taxes_id = taxes_id.filtered(lambda x: x.company_id.id == self.company_id.id)

		price_unit = self.env['account.tax']._fix_tax_included_price_company(seller.price, self.product_id.supplier_taxes_id, taxes_id, self.company_id) if seller else 0.0
		if price_unit and seller and po.currency_id and seller.currency_id != po.currency_id:
			price_unit = seller.currency_id.compute(price_unit, po.currency_id)

		product_lang = self.product_id.with_context({
			'lang': supplier.name.lang,
			'partner_id': supplier.name.id,
		})
		name = product_lang.display_name
		if product_lang.description_purchase:
			name += '\n' + product_lang.description_purchase

		date_planned = self.env['purchase.order.line']._get_date_planned(seller, po=po).strftime(DEFAULT_SERVER_DATETIME_FORMAT)

		return {
			'name': name,
			'product_qty': procurement_uom_po_qty,
			'product_id': self.product_id.id,
			'product_uom': self.product_uom.id,
			'price_unit': price_unit,
			'date_planned': date_planned,
			'taxes_id': [(6, 0, taxes_id.ids)],
			'procurement_ids': [(4, self.id)],
			'order_id': po.id,
		}

	def _make_po_get_domain(self, partner):
		gpo = self.rule_id.group_propagation_option
		group = (gpo == 'fixed' and self.rule_id.group_id) or \
				(gpo == 'propagate' and self.group_id) or False

		domain = (
			('partner_id', '=', partner.id),
			('state', '=', 'draft'),
			('is_merger', '=', False),
			('origin', '=', ''),
			('picking_type_id', '=', self.rule_id.picking_type_id.id),
			('company_id', '=', self.company_id.id),
			('dest_address_id', '=', self.partner_dest_id.id))
		print"-------domain-------custo---------",domain
		if group:
			domain += (('group_id', '=', group.id),)
		return domain

class Picking(models.Model):
	_inherit = "stock.picking"

	so_no = fields.Many2one('sale.order', string='Sale Order')
	cartage = fields.Float('Cartage')
	packing= fields.Float('Packing')
	others = fields.Float('Others')
	_order = "min_date desc" 

	@api.multi
	def do_prepare_partial(self):
		# TDE CLEANME: oh dear ...
		PackOperation = self.env['stock.pack.operation']

		# get list of existing operations and delete them
		existing_packages = PackOperation.search([('picking_id', 'in', self.ids)])  # TDE FIXME: o2m / m2o ?
		if existing_packages:
			existing_packages.unlink()
		for picking in self:
			forced_qties = {}  # Quantity remaining after calculating reserved quants
			picking_quants = self.env['stock.quant']
			# Calculate packages, reserved quants, qtys of this picking's moves
			for move in picking.move_lines:
				if move.state not in ('assigned', 'confirmed', 'waiting'):
					continue
				move_quants = move.reserved_quant_ids
				picking_quants += move_quants
				forced_qty = 0.0
				if move.state == 'assigned':
					qty = move.product_uom._compute_quantity(move.product_uom_qty, move.product_id.uom_id, round=False)
					forced_qty = qty - sum([x.qty for x in move_quants])
				# if we used force_assign() on the move, or if the move is incoming, forced_qty > 0
				if float_compare(forced_qty, 0, precision_rounding=move.product_id.uom_id.rounding) > 0:
					if forced_qties.get(move.product_id):
						forced_qties[move.product_id] += forced_qty
					else:
						forced_qties[move.product_id] = forced_qty
			for vals in picking._prepare_pack_ops(picking_quants, forced_qties):
				vals['fresh_record'] = False
				PackOperation |= PackOperation.create(vals)
		# recompute the remaining quantities all at once
			for mv in picking.move_lines:
				PackOperation.write({'product_uom_id': mv.product_uom.id})
		self.do_recompute_remaining_quantities()
		for pack in PackOperation:
			pack.ordered_qty = sum(
				pack.mapped('linked_move_operation_ids').mapped('move_id').filtered(lambda r: r.state != 'cancel').mapped('ordered_qty')
			)
		self.write({'recompute_pack_op': False})

class StockPackOperation(models.Model):
	_inherit = "stock.pack.operation"

	bill_no = fields.Char(string='Bill No.')
	bill_date = fields.Date('Bill Date')
	batch_no = fields.Char('Batch No.')
	mfg_date = fields.Date('Date of MFG')
	expiry_date = fields.Date('Expiry Date')
	steriliz_ref = fields.Char('Sterilization Ref')




