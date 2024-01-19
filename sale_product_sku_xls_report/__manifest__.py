# -*- coding: utf-8 -*-
{
    'name': 'Export Sale Product sku Excel',
    'version': '1.0.0',
    'category': 'Account',
    'summary': '''
        Prints Excel Report based on sale order.
        ''',
    'author': 'Rajeev Kumar',
    'license': "",
    'depends': [
        'base','web','sale','account',
    ],
    'data': [
		'security/ir.model.access.csv',
        'wizard/sale_product_sku_view.xml'
    ],
    'demo': [],  
    'auto_install': False,
    'installable': True,
    'application': True
}
