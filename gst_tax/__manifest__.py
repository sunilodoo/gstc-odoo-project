# -*- coding: utf-8 -*-

{
    "name" : "GST Taxation System",
    "version" : "1.0",
    "author" : "Rajeev Kumar",
    "description": """
	Add GST Tax based on Warehouse and Customer state.
	""",
    "website" : "",
    "category" : "Sale,Purchase,Account",
	"summary" : "GST Taxation System",
    "depends": ['base' ,'sale', 'purchase'],
    "data" : [
	   "view/gst_view.xml",
	   "security/ir.model.access.csv",
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
}
