# -*- coding: utf-8 -*-
{
    'name': 'Sale Order Excel Report',
    'version': '1.0.0',
    'category': 'Sale',
    'summary': '''
        Prints Excel Report based on sale order salesperson and date wise.
        ''',
    'author': 'Rajeev Kumar',
    'depends': [
        'sale'
    ],
    'data': [
        'wizard/sale_order_xls_view.xml'
    ],
    'demo': [],  
    'images': ['static/description/banner.png'],
    'auto_install': False,
    'installable': True,
    'application': True
}
