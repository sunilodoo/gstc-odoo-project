# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _

class ProductTemplate(models.Model):
    _inherit = "product.template"

    uom_conversion_ids = fields.One2many('product.uom.conversion', 'product_template_id', string="UoM Conversion")
