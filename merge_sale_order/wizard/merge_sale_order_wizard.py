# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class MergeSaleOrder(models.TransientModel):
    _name = 'merge.sale.order'

    merge_type = \
        fields.Selection([
            ('new_cancel',
                'Create new PI and cancel all selected PI'),
            ('merge_cancel',
             'Merge PI on existing selected PI and cancel others'),],
            default='new_cancel')
    sale_order_id = fields.Many2one('sale.order', 'PI')

    @api.onchange('merge_type')
    def onchange_merge_type(self):
        res = {}
        for order in self:
            order.sale_order_id = False
            if order.merge_type in ['merge_cancel']:
                sale_orders = self.env['sale.order'].browse(
                    self._context.get('active_ids', []))
                res['domain'] = {
                    'sale_order_id':
                    [('id', 'in',
                        [sale.id for sale in sale_orders])]
                }
            return res

    @api.multi
    def merge_orders(self):
        buyer_ref = ''
        buyer_date = ''
        target_year = False
        incoterm = ''
        payment_term_id = ''
        dil_date = ''
        delivery_time = ''
        payment_detail = ''
        carrier_id = False
        freight_charge = 0
        freight_only = 0
        insurance_only = 0
        bank_charge = 0
        global_disc = 0
        chrgs_inf = ''
        ext_chrgs = 0
        show_disc = False
        show_ex_chrgs = False
        sale_orders = self.env['sale.order'].browse(
            self._context.get('active_ids', []))
        existing_so_line = False
        if len(self._context.get('active_ids', [])) < 2:
            raise UserError(
                _('Please select atleast two PI to perform '
                    'the Merge Operation.'))
        if any(order.state not in ['draft','sent','sale'] for order in sale_orders):
            raise UserError(
                _('Please select PI which are in PI/Confirmed state '
                  'to perform the Merge Operation.'))
        partner = sale_orders[0].partner_id.id
        if any(order.partner_id.id != partner for order in sale_orders):
            raise UserError(
                _('Please select PI whose Customers are same to '
                    ' perform the Merge Operation.'))
        if self.merge_type == 'new_cancel':
            print"---self._context----",self._context
            so = self.env['sale.order'].with_context({
                'trigger_onchange': True,
                'onchange_fields_to_trigger': [partner]
            }).create({'partner_id': partner})
            default = {'order_id': so.id}
            print"---so----",so
            
            for order in sale_orders:
            	buyer_ref = order.buyer_ref and buyer_ref +', '+ order.buyer_ref or ''
            	buyer_date = order.buyer_date and order.buyer_date or ''
            	target_year = order.target_year and order.target_year.id or ''
            	incoterm = order.incoterm and order.incoterm.id or ''
            	payment_term_id = order.payment_term_id and order.payment_term_id.id or ''
            	dil_date = order.dil_date and order.dil_date or ''
            	delivery_time = order.delivery_time and order.delivery_time.id or ''
            	payment_detail = order.payment_detail and order.payment_detail or ''
            	carrier_id = order.carrier_id and order.carrier_id.id or ''
            	freight_charge = freight_charge + order.freight_charge
            	freight_only = freight_only + order.freight_only
            	insurance_only = insurance_only + order.insurance_only
            	bank_charge = bank_charge + order.bank_charge
            	global_disc = global_disc + order.global_disc
            	ext_chrgs = ext_chrgs + order.ext_chrgs
            	chrgs_inf = order.chrgs_inf and chrgs_inf +', '+ order.chrgs_inf or ''
            	show_disc = order.show_disc
            	show_ex_chrgs = order.show_ex_chrgs
                for line in order.order_line:
                    existing_so_line = False
                    if so.order_line:
                        for soline in so.order_line:
                            if line.product_id == soline.product_id and \
                                    line.price_unit == soline.price_unit:
                                existing_so_line = soline
                                break
                    if existing_so_line:
                        existing_so_line.product_uom_qty += \
                            line.product_uom_qty
                        so_taxes = [
                            tax.id for tax in existing_so_line.tax_id]
                        [so_taxes.append((tax.id))
                         for tax in line.tax_id]
                        existing_so_line.tax_id = \
                            [(6, 0, so_taxes)]
                    else:
                        line.copy(default=default)
            so.write({'buyer_ref': buyer_ref, 'buyer_date': buyer_date, 'target_year': target_year, 'incoterm': incoterm, 'payment_term_id': payment_term_id, 'dil_date': dil_date, 'delivery_time': delivery_time, 'payment_detail': payment_detail, 'carrier_id': carrier_id, 'freight_charge': freight_charge, 'freight_only': freight_only, 'insurance_only': insurance_only, 'bank_charge': bank_charge, 'global_disc': global_disc, 'ext_chrgs': ext_chrgs, 'chrgs_inf': chrgs_inf, 'show_disc': show_disc, 'show_ex_chrgs': show_ex_chrgs})
            for order in sale_orders:
                order.action_cancel()
                order.remarks = 'merged in PI No.: '+ str(so.name)
        elif self.merge_type == 'merge_cancel':
            default = {'order_id': self.sale_order_id.id}
            so = self.sale_order_id
            for order in sale_orders:
                if order == so:
                    continue
                buyer_ref = order.buyer_ref and buyer_ref +', '+ order.buyer_ref or ''
            	buyer_date = order.buyer_date and order.buyer_date or ''
            	target_year = order.target_year and order.target_year.id or ''
            	incoterm = order.incoterm and order.incoterm.id or ''
            	payment_term_id = order.payment_term_id and order.payment_term_id.id or ''
            	dil_date = order.dil_date and order.dil_date or ''
            	delivery_time = order.delivery_time and order.delivery_time.id or ''
            	payment_detail = order.payment_detail and order.payment_detail or ''
            	carrier_id = order.carrier_id and order.carrier_id.id or ''
            	freight_charge = freight_charge + order.freight_charge
            	freight_only = freight_only + order.freight_only
            	insurance_only = insurance_only + order.insurance_only
            	bank_charge = bank_charge + order.bank_charge
            	global_disc = global_disc + order.global_disc
            	ext_chrgs = ext_chrgs + order.ext_chrgs
            	chrgs_inf = order.chrgs_inf and chrgs_inf +', '+ order.chrgs_inf or ''
            	show_disc = order.show_disc
            	show_ex_chrgs = order.show_ex_chrgs
                for line in order.order_line:
                    existing_so_line = False
                    if so.order_line:
                        for soline in so.order_line:
                            if line.product_id == soline.product_id and \
                                    line.price_unit == soline.price_unit:
                                existing_so_line = soline
                                break
                    if existing_so_line:
                        existing_so_line.product_uom_qty += \
                            line.product_uom_qty
                        so_taxes = [
                            tax.id for tax in existing_so_line.tax_id]
                        [so_taxes.append((tax.id))
                         for tax in line.tax_id]
                        existing_so_line.tax_id = \
                            [(6, 0, so_taxes)]
                    else:
                        line.copy(default=default)
            so.write({'buyer_ref': buyer_ref, 'buyer_date': buyer_date, 'target_year': target_year, 'incoterm': incoterm, 'payment_term_id': payment_term_id, 'dil_date': dil_date, 'delivery_time': delivery_time, 'payment_detail': payment_detail, 'carrier_id': carrier_id, 'freight_charge': freight_charge, 'freight_only': freight_only, 'insurance_only': insurance_only, 'bank_charge': bank_charge, 'global_disc': global_disc, 'ext_chrgs': ext_chrgs, 'chrgs_inf': chrgs_inf, 'show_disc': show_disc, 'show_ex_chrgs': show_ex_chrgs})
            for order in sale_orders:
                if order != so:
                    order.sudo().action_cancel()
                    order.remarks = 'merged in PI No.: '+ str(so.name)
