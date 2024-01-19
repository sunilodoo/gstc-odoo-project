# -*- coding: utf-8 -*-
{
    'name' : 'Sale Order Excel Report',
    'version': '10.0',
    'author': 'Rajeev Kumar',
    'category': 'Sale',
    'website': '',
    'summary': 'Excel sheet for Sale Order',
    'description': """ Excel sheet for Sale Order""",
    'depends': [
        'base','sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/sale_order_xls_view.xml',
    ],
    'images': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
