# -*- coding: utf-8 -*-

{
    'name': 'Paramount Import Customers',
    'version': '1.0',
    'category': 'Tools',
    'author': 'Rajeev Kumar',
    'website': '',
    'summary': 'Import Customers',
    'description': """
        Import Customers From CSV File.
    """,
    'images': [],
    'depends': ['base', 'sale'],
    'data': [
            'views/import_customers_view.xml',
			'Security/ir.model.access.csv',
     ],
    'installable': True,
}
