# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
{
    'name': 'Web Widget Multiple Image V10',
    'version': '10.0.0.0.1',
    'author': 'Rajeev Kumar',
    'maintainer': 'Rajeev Kumar',
    'category': 'Image',
    'complexity': 'easy',
    'depends': ['product','dusal_web_tree_image'],
    'license': 'AGPL-3',
    'summary': 'Multiple web images widget',
    'data': [
        'view/templates.xml',
        'view/product_view.xml',
		'Security/ir.model.access.csv',
    ],
    'website': '',
    'qweb': ['static/src/xml/image_multi.xml'],
    'installable': True,
    'auto_install': False,
}
