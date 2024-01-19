{
    'name': 'Hide Menu User Wise',
    'version': '1.0',
    'category': 'Extra Tools',
    'summary': """Hide Menu User Wise""",
    'description': 'Hide Menu User Wise,Hide Menu',
    'author': 'GST Corporation Ltd',
    'company': 'GST Corporation Ltd',
    'maintainer': 'GST Corporation Ltd',
     'website':'https://www.gstc.com/',
    'depends': ['base'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/hide_user_menu.xml',
        'wizard/import_list_menu_view.xml',
    ],
    "external_dependencies": {
        "python": [
                # "openpyxl",
        ],
    },
    'images': [
    	# 'static/description/banner.png'
    ],
      'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
    'assets': {},
    'license': 'LGPL-3'
}
