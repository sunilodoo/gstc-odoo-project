# -*- coding: utf-8 -*-

{
    "name" : "GSTC Stock",
    "version" : "1.0",
    "author" : "Rajeev Kumar",
    "description": """
	To maintain stock for GSTC Server.
	""",
    "website" : "",
    "category" : "Sale,Purchase,Account,Stock",
	"summary" : "GSTC Stock",
    "depends": ['base' ,'sale', 'purchase', 'stock'],
    "data" : [
	   "view/gst_stock_view.xml",
	   "view/gstc_invoice_view.xml",
	   #"security/ir.model.access.csv",
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
}
