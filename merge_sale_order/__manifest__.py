# -*- coding: utf-8 -*-

{
    'name': 'Merge Sale Order',
    'category': 'Sales',
    'summary': 'This module will merge sale order.',
    'version': '1.0',
    'website': '',
    'author': 'Rajeev Kumar',
    'description': 'Merge Sale Order',
    'depends': [
        'sale'
    ],

    'data': [
        'wizard/merge_sale_order_wizard_view.xml',
        'security/ir.model.access.csv',
    ],
    'auto_install': False,
    'installable': True,
    'application': False

}
