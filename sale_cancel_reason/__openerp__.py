# -*- coding: utf-8 -*-
#
#
#    Author: Sharique Anwer
#    Copyright 2016 Healthgenie India Pvt. Ltd.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

{
    'name': 'Sale Cancel Reason',
    'version': '9.0.1.0.0',
    'author': 'Sharique Anwer - Healthgenie',
    'category': 'Sale',
    'license': 'AGPL-3',
    'complexity': 'normal',
    'website': "http://www.healthgenie.in",
    'description': """
Sale Cancel Reason
==================

When a sale order is cancelled, a reason must be given,
it is chosen from a configured list.

""",
    'depends': ['sale'],
    'data': ['wizard/cancel_reason_view.xml',
             'views/sale_view.xml',
             'security/ir.model.access.csv',
             'data/sale_order_cancel_reason.xml',
             ],
    'test': ['test/sale_order_cancel.yml'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
