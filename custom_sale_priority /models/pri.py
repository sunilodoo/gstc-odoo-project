# -*- coding: utf-8 -*-
#############################################################################
from openerp import models, fields, osv, api, _
from openerp.tools.translate import _
from openerp import netsvc
from datetime import datetime, timedelta

class sale_order(models.Model):
    _inherit = "sale.order"
    _order = 'sequence'
    sequence = fields.Integer(string='Sequence', default=10)

class purchase_order(models.Model):
    _inherit = "purchase.order"
    _order = 'sequence'
    sequence = fields.Integer(string='Sequence', default=10)

