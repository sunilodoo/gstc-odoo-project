# -*- coding: utf-8 -*-
{
    "name": "Multiple UOM in Sale Order",
    "version": "16.0.0.0",
    "author": "Bytelegion",
    "website": "http://www.bytelegions.com",
    "depends": ["base", "stock", 'stock_account', 'sale'],
    "license": "AGPL-3",
    "category": "Tools",
    'company': 'Bytelegion',

    # "summary": """This Module used to Compute Salary for Employees.""",
    # "description": """This Module used to Compute Salary for Employees.""",

    "data": [

        'views/sale_view.xml',

    ],

    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.gif'], 
    
}
