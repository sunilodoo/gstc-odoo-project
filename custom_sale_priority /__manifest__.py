# -*- coding: utf-8 -*-

{
    "name" : "Custom Sale Priority",
    "version" : "1.0",
    "author" : "Healthgenie",
    "description": """Add a Approve or Refuse Button For approval of a Sale Quotation""",
    "website" : "",
    "category" : "Sale",
	"summary" : "Double validation for a quotation",
    "depends": ['base' ,'sale','purchase',],
    "data" : [
	   "view/pri_view.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
}
