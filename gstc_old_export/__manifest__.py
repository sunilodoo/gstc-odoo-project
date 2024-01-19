# -*- coding: utf-8 -*-

{
    "name" : "GSTC Old Export/Commercial/Packing List",
    "version" : "1.0",
    "author" : "Rajeev Kumar",
    "description": """
	To maintain stock for GSTC Old Export/Commercial/Packing List.
	""",
    "website" : "",
    "category" : "Sale,Purchase,Account,Stock",
	"summary" : "GSTC Old Export/Commercial/Packing List",
    "depends": ['base' ,'sale', 'purchase', 'stock'],
    "data" : [
	   "view/gstc_old_exprot_view.xml",
	   "view/shipping_panel_view.xml",
	   "view/procurement_panel_view.xml",
	   "security/ir.model.access.csv",
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
}
