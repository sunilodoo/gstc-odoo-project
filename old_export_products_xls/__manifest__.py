# -*- coding: utf-8 -*-
{
    'name': 'Old Export Products Excel',
    'version': '1.0.0',
    'category': 'Account',
    'summary': '''
        Prints Excel Report based on Executed Sales By Products to Buyar.
        ''',
    'author': 'Santosh Singh',
    'license': "",
    'depends': [
        'base','web','sale','account',
    ],
    'data': [
		'security/ir.model.access.csv',
        'wizard/executed_sale_products_view.xml'
    ],
    'demo': [],  
    'auto_install': False,
    'installable': True,
    'application': True
}
