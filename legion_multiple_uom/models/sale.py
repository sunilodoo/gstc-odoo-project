# -*- coding: utf-8 -*-
import calendar

from odoo import tools, api, models, _, fields
from odoo.exceptions import UserError
from odoo.tools import config
from odoo.exceptions import ValidationError
import datetime as dt
from datetime import datetime

from odoo.api import onchange


class SaleOrderLine(models.Model):
    _inherit = "sale.order"

    # @api.multi
    def _action_confirm(self):
        location = self.env.ref('stock.stock_location_stock')

        for line in self.order_line:
            product = line.product_id
            qty = line.grand
            updated_qty = self.env['stock.quant']._update_available_quantity(product, location, -qty)
            print('Updated Subtract Quantity', updated_qty)


class ClassSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_uom_1 = fields.Many2one('uom.uom', string='Secondary UOM')
    piece = fields.Float(string="Extra Piece", required=False, default=1)

    grand = fields.Float(string="Total QTY", required=False, readonly=True)

    ratio_con_1 = fields.Float(string="Ration Convert 1", required=False, readonly=True)
    ratio_con_2 = fields.Float(string="Ration Convert 2", required=False, readonly=True)

    @api.onchange('product_uom_1', 'product_uom')
    def _second_uom(self):
        for order in self:
            temp_1 = 0
            temp_2 = 0
            grand = 0

            for rec in order:
                temp_1 = rec.product_uom.factor_inv
                temp_2 = rec.product_uom_1.factor_inv

                rec.ratio_con_1 = temp_1
                rec.ratio_con_2 = temp_2

                if temp_1 > 0:
                    test_1 = rec.piece * temp_2
                    test_2 = test_1 / temp_1
                    rec.grand = test_2 + rec.product_uom_qty

                    # rec.price_subtotal = rec.grand * rec.price_unit

                rec.price_subtotal = rec.grand * rec.price_unit

                print("Temp 1: ", temp_1)
                print("Temp 2: ", temp_2)

                print("Ratio of 1st UOM: ", rec.product_uom.factor_inv)
                print("Ratio of 2nd UOM: ", rec.product_uom_1.factor_inv)
