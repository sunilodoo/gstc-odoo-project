{
    'name': 'Whatsapp Odoo Chat',
    'version': '10.0.0.1',
    'summary': 'Whatsapp Odoo Chat',
    'author': 'Rajeev Kumar',
    'company': '',
    'description': """Whatsapp Odoo Chat""",
    'category': 'Connector',
    'depends': [
        'base', 'contacts', 'sale', 'crm', 'stock', 'account', 'purchase'
    ],
    'data': [
        'security/ir.model.access.csv',
        'models/whatsapp_template.xml',
        'views/whatsapp_button_views.xml',
        'wizard/whatsapp_wizard.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
