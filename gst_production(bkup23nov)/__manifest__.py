# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'GST Custom',
    'version': '1.2',
    'author': "AJAY KHANNA",
    'category': 'Sales',
    'sequence': 60,
    'summary': 'Sale Orders, Receipts, Vendor Bills',
    'description': """
Manage goods requirement by Purchase Orders easily
==================================================

Purchase management enables you to track your vendors' price quotations and convert them into purchase orders if necessary.
Odoo has several methods of monitoring invoices and tracking the receipt of ordered goods. You can handle partial deliveries in Odoo, so you can keep track of items that are still to be delivered in your orders, and you can issue reminders automatically.

    """,
    'website': 'https://www.odoo.com/page/purchase',
    'depends': ['stock_account', 'report'],
    'data': [
        'Security/ir.model.access.csv',
        'views/gst_production.xml',
        'views/sale_order_report.xml',
        'views/account_invoice_report.xml',
		'views/layout_last_page.xml',
		'views/layouts.xml',
        
    ],
    'test': [
        
    ],
    'demo': [
       
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
