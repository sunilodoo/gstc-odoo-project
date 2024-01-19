# -*- coding: utf-8 -*-


{
    'name': "Import Products",
    'summary': """This module allow you to Import Products from CSV file""",
    'description': """
		Import Products from CSV .

    """,
    'author': "Rajeev Kumar.",
    'website': "",
    'images': [],
    'version': '1.0',
    'category' : 'sale',
    'depends': ['base','sale', 'para_import_customers'],
    'data':[
        'views/import_products_view.xml',
        'views/export_product_view.xml',
        'data/product_demo.xml',
    ],
    'installable' : True,
    'application' : False,
    'auto_install' : False,
}
