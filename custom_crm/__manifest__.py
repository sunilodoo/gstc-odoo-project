# -*- coding: utf-8 -*-


{
    'name': "Custom CRM",
    'summary': """ Customize CRM Lead""",
    'description': """
Customize CRM Lead
    """,
    'author': "Santosh Singh",
    'website': "",
    'images': [],
    'version': '1.0',
    'category' : 'sale',
    'depends': ['base','sale', 'crm', 'custom_product_fields', 'custom_task_view'],
    # 'depends': ['base','sale', 'purchase','project'],
    'data':[
        'views/res_partner_view.xml',
        # 'views/custom_task_view.xml',
        'views/custom_lead_view.xml',
        'wizard/crm_lead_export_view.xml',
        'wizard/crm_lead_import_view.xml',
		'Security/ir.model.access.csv',
    ],
    'installable' : True,
    'application' : True,
    'auto_install' : False,
}
