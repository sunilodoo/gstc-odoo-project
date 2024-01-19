# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import xlwt
import datetime
import unicodedata
import base64
import StringIO
import csv, cStringIO
from datetime import datetime
from odoo import api, fields, models, _
import platform
from collections import defaultdict


class InvoiceReportOut(models.Model):        
    _name = 'invoice.report.out'
    _description = 'Commercial Invoice Report'
    
    invoice_data = fields.Char('Name', size=256)
    file_name = fields.Binary('CI Excel Report', readonly=True)
    invoice_work = fields.Char('Name', size=256)
    file_names = fields.Binary('CI CSV Report', readonly=True)
    
   
class CIWizards(models.Model):        
    _name = 'commercial.reports'
    _description = 'Commercial wizard'
    
#purchase order excel report button actions
    @api.multi
    def get_order(self):
		invoice = self.env['account.invoice'].browse(self._context.get('active_ids', list()))
		for inv in invoice:
			so = self.env['sale.order'].search([('name','=',inv.origin)])
			result = []
			result.append({'mode_of_ship': so.carrier_id.name, 'delivery_term': so.incoterms.name})
			print"---------result----=====----result---",result
		return result

    @api.multi
    def get_qty(self):
		result = []
		c = defaultdict(int)
		invoice = self.env['account.invoice'].browse(self._context.get('active_ids', list()))
		for inv in invoice:
			for line in inv.invoice_line_ids:
				if line.uom_id:
					print"---------line.uom_id.name===",line.uom_id.name
					result.append({'name':line.uom_id.name, 'value': line.quantity})
		print"---------result----=====----get_qty---",result
		for d in result:
			c[d['name']] += d['value']
		return [{'name': name, 'value': val} for name, val in c.items()]
               
    @api.multi
    def action_commercial_report(self):          
#XLS report         
        custom_value = {}
        label_lists=['PO','POR','CLIENTREF','BARCODE','DEFAULTCODE','NAME','QTY','VENDORPRODUCTCODE','TITLE', 'PARTNERNAME', 'EMAIL', 'PHONE', 'MOBILE', 'STREET', 'STREET2', 'ZIP', 'CITY', 'COUNTRY']                    
        order = self.env['account.invoice'].browse(self._context.get('active_ids', list()))      
        workbook = xlwt.Workbook()                      
        for rec in order:              
            invoice = []                                                          
            for line in rec.invoice_line_ids: 
                if line.quantity > 0:                           
                    product = {}                                                                       
                    product ['product_id'] = line.name                                                                            
                    product ['product_qty'] = line.quantity                           
                    product ['uom'] = line.uom_id.name                          
                    product ['price_unit'] = '{0:.4f}'.format(line.price_unit)                      
                    product ['price_subtotal'] = '{0:.2f}'.format(line.price_subtotal)                       
                    invoice.append(product)
                                                                                           
            custom_value['products'] = invoice               
            custom_value ['partner_id'] = rec.partner_id.name
            custom_value ['partner_ref'] = ''
            custom_value ['payment_term_id'] = rec.payment_term_id.name
            custom_value ['date_order'] = rec.date_invoice
            custom_value ['partner_no'] = rec.name
            custom_value ['amount_total'] = str(rec.amount_total)+' '+rec.currency_id.symbol
            custom_value ['amount_untaxed'] = str(rec.amount_untaxed)+' '+rec.currency_id.symbol
            custom_value ['amount_tax'] = str(rec.amount_tax)+' '+rec.currency_id.symbol
                                                  
            style0 = xlwt.easyxf('font: name Times New Roman bold on;align: horiz right;borders: bottom_color black, top_color black, right_color black, left_color black,left thin, right thin, bottom thin, top thin;', num_format_str='#,##0.00')
            style1 = xlwt.easyxf('font: name Times New Roman bold on;align: horiz center;borders: bottom_color black, top_color black, right_color black, left_color black,left thin, right thin, bottom thin, top thin;', num_format_str='#,##0.00')
            style2 = xlwt.easyxf('font:height 400,bold True;align: horiz center;borders: top_color black, bottom_color black, right_color black, left_color black,left thin, right thin, top thin, bottom thin;', num_format_str='#,##0.00')         
            style3 = xlwt.easyxf('font:bold True;', num_format_str='#,##0.00')
            style4 = xlwt.easyxf('font:bold True;  borders:top double;align: horiz right;', num_format_str='#,##0.00')
            style5 = xlwt.easyxf('font: name Times New Roman bold on;align: horiz center;borders: bottom_color black, top_color black, right_color black, left_color black,left thin, right thin, bottom thin, top thin;', num_format_str='#,##0')
            style6 = xlwt.easyxf('font: name Times New Roman bold on;borders: bottom_color black, top_color black, right_color black, left_color black,left thin, right thin, bottom thin, top thin;', num_format_str='#,##0.00')
            style7 = xlwt.easyxf('font:bold True;  borders:top double;', num_format_str='#,##0.00')
            style8 = xlwt.easyxf('font:name Times New Roman;align: horiz left;borders: bottom_color black, right_color black, left_color black,left thin, right thin, bottom thin;', num_format_str='#,##0.00') 
            style9 = xlwt.easyxf('font:height 200,bold True;align: horiz left;borders: top_color black, right_color black, left_color black,left thin, right thin, top thin;', num_format_str='#,##0.00') 
            style10 = xlwt.easyxf('font:height 0,bold off;align: horiz left;borders: right_color black,right thin;', num_format_str='#,##0.00') 
            style11 = xlwt.easyxf('font:height 200,bold True;align: horiz left;borders: bottom_color black, top_color black, right_color black, left_color black,left thin, right thin, bottom thin, top thin;', num_format_str='#,##0.00') 
            style12 = xlwt.easyxf('font:height 200,bold True;align: horiz right;borders: top_color black, right_color black, left_color black,left thin, right thin, top thin;', num_format_str='#,##0.00') 
                          
            sheet = workbook.add_sheet(rec.inv_no or 'Commercial Invoice')
            sheet.write_merge(0, 1, 0, 11, 'Commercial Invoice', style2)
            
            #sheet.write_merge(2, 3, 4, 6, 'Invoice No :', style2)
            #sheet.write_merge(2, 3, 7, 8, custom_value['partner_no'], style2)    
            sheet.write_merge(2, 2, 0, 5, 'EXPORTER', style9)
            sheet.write_merge(3, 8, 0, 5, rec.company_id.partner_id.name +'\n'+ rec.company_id.partner_id.street +'\n'+ 
                rec.company_id.partner_id.street2 +'\n'+ rec.company_id.partner_id.city +' '+ rec.company_id.partner_id.zip +' '+
                rec.company_id.partner_id.country_id.name +'\n'+
                (rec.company_id.partner_id.email and 'Email: '+str(rec.company_id.partner_id.email) or '') +'\n'+ 
                (rec.company_id.partner_id.phone and 'Phone: '+str(rec.company_id.partner_id.phone) or '') +''+
                (rec.company_id.partner_id.fax and ', Fax: '+str(rec.company_id.partner_id.fax) or '') +'\n'+ 
                (rec.company_id.partner_id.gstn and 'GSTIN: '+str(rec.company_id.partner_id.gstn) or ''), style8)

            sheet.write_merge(2, 2, 6, 7, 'Invoice No.& Date:', style8)
            sheet.write_merge(2, 2, 8, 11, (rec.inv_no and rec.inv_no or '') + ' DT. ' +(rec.date_invoice and datetime.strptime(rec.date_invoice,'%Y-%m-%d').strftime("%d.%m.%Y") or ''), style8) 
            sheet.write_merge(3, 3, 6, 7, "Buyer's Order No.& Date:", style8) 
            sheet.write_merge(3, 3, 8, 11, (rec.order_no and str(rec.order_no) or '') + ' DT. ' + (rec.order_date and datetime.strptime(rec.order_date,'%Y-%m-%d').strftime("%d.%m.%Y") or ''), style8) 
            sheet.write_merge(4, 4, 6, 7, 'Country Of Origin:', style8) 
            sheet.write_merge(4, 4, 8, 11, rec.origin_country or '', style8) 
            sheet.write_merge(5, 5, 6, 7, 'Country Of Destination:', style8) 
            sheet.write_merge(5, 5, 8, 11, rec.dest_country and rec.dest_country.name or '', style8)
            sheet.write_merge(6, 6, 6, 7, 'Mode Of Shipment:', style8)
            sheet.write_merge(6, 6, 8, 11, rec.carrier_id and rec.carrier_id.name or '', style8)
            sheet.write_merge(7, 7, 6, 7, 'Nature Of Payment:', style8)
            sheet.write_merge(7, 7, 8, 11, rec.payment_term_id and rec.payment_term_id.name or '', style8)
            sheet.write_merge(8, 8, 6, 7, 'Terms Of Delivery:', style8)
            sheet.write_merge(8, 8, 8, 11, rec.incoterms and rec.incoterms.name or '', style8)
            #sheet.write_merge(9, 9, 6, 7, rec.date_invoice, style3)
            #sheet.write_merge(9, 9, 8, 11, rec.date_invoice, style3)
            #sheet.write(2, 0, 'EXPORTER:', style3)
            #sheet.write(2, 1, custom_value['partner_id'], style0)     
            #sheet.write_merge(5, 5, 8, 9, 'Order  Date', style3)
            #sheet.write_merge(5, 5, 10, 11, custom_value['date_order'], style0)     
            #sheet.write_merge(6, 6, 8, 9, 'Vendor Reference', style3)
            #sheet.write_merge(6, 6, 10, 11, custom_value['partner_ref'], style0)
            #sheet.write_merge(7, 7, 8, 9, 'Payment Terms', style3)
            #sheet.write_merge(7, 7, 10, 11, custom_value['payment_term_id'], style0)

            #sheet.write(10, 1, 'S NO', style1)                           
            #sheet.write_merge(10, 10, 2, 3, 'PRODUCT', style1)
            #sheet.write_merge(10, 10, 4, 5, 'QUANTITY', style1)        
            #sheet.write_merge(10, 10, 6, 7, 'UNIT PRICE', style1)
            #sheet.write_merge(10, 10, 8, 10, 'TAXES', style1) 
            #sheet.write(10, 11, 'SUBTOTAL', style1)
            sheet.write_merge(9, 9, 0, 5, 'Consignee', style9)
            if rec.is_consignee and rec.consignee and (rec.partner_id != rec.consignee) :
                sheet.write_merge(10, 17, 0, 5, rec.consignee.name +'\n'+ 
                    str(rec.consignee.street) +'\n'+ str(rec.consignee.street2) +'\n'+ 
                    str(rec.consignee.city) +' '+ str(rec.consignee.zip) +' '+ str(rec.consignee.country_id.name) +'\n'+ 
                	(rec.consignee.partner_vat_name and rec.consignee.vat and str(rec.consignee.partner_vat_name) +str(rec.consignee.vat) or '') +'\n'+
                	(rec.consignee.email and 'Email: '+str(rec.consignee.email) or '') +'\n'+ 
                	(rec.consignee.phone and 'Phone: '+str(rec.consignee.phone) or '') +''+ 
                	(rec.consignee.fax and ', Fax: '+str(rec.consignee.fax) or '') , style8)
            if rec.is_consignee and rec.consignee and (rec.partner_id == rec.consignee) : 
                sheet.write_merge(10, 17, 0, 5, rec.partner_id.name +'\n'+ 
                    str(rec.partner_id.street) +'\n'+ str(rec.partner_id.street2) +'\n'+ 
                    str(rec.partner_id.city) +' '+ str(rec.partner_id.zip) +' '+ str(rec.partner_id.country_id.name) +'\n'+ 
					(rec.partner_id.partner_vat_name and rec.partner_id.vat and str(rec.partner_id.partner_vat_name) +str(rec.partner_id.vat) or '') +'\n'+
		            (rec.partner_id.email and 'Email: '+str(rec.partner_id.email) or '') +'\n'+ 
		            (rec.partner_id.phone and 'Phone: '+str(rec.partner_id.phone) or '') +''+ 
		            (rec.partner_id.fax and ', Fax: '+str(rec.partner_id.fax) or '') , style8)
            if not rec.is_consignee :
                sheet.write_merge(10, 17, 0, 5, rec.partner_id.name +'\n'+ 
                    str(rec.partner_id.street) +'\n'+ str(rec.partner_id.street2) +'\n'+ 
                    str(rec.partner_id.city) +' '+ str(rec.partner_id.zip) +' '+ str(rec.partner_id.country_id.name) +'\n'+ 
					(rec.partner_id.partner_vat_name and rec.partner_id.vat and str(rec.partner_id.partner_vat_name) +str(rec.partner_id.vat) or '') +'\n'+
		            (rec.partner_id.email and 'Email: '+str(rec.partner_id.email) or '') +'\n'+ 
		            (rec.partner_id.phone and 'Phone: '+str(rec.partner_id.phone) or '') +''+ 
		            (rec.partner_id.fax and ', Fax: '+str(rec.partner_id.fax) or '') , style8)
            sheet.write_merge(9, 9, 6, 11, 'Buyer(if other than consignee)', style9)
            sheet.write_merge(10, 17, 6, 11, rec.partner_id.name +'\n'+ str(rec.partner_id.street) +'\n'+ 
                str(rec.partner_id.street2) +'\n'+ str(rec.partner_id.city) +' '+ 
                (rec.partner_id.zip and str(rec.partner_id.zip) or '') +' '+ str(rec.partner_id.country_id.name) +'\n'+ 
				(rec.partner_id.partner_vat_name and rec.partner_id.vat and str(rec.partner_id.partner_vat_name) +str(rec.partner_id.vat) or '') +'\n'+
                (rec.partner_id.email and 'Email: '+str(rec.partner_id.email) or '') +'\n'+ 
                (rec.partner_id.phone and 'Phone: '+str(rec.partner_id.phone) or '') +''+ 
                (rec.partner_id.fax and ', Fax: '+str(rec.partner_id.fax) or '') , style8)
            sheet.write_merge(18, 18, 0, 2, 'Pre-carrier By:', style8)
            sheet.write_merge(18, 18, 3, 5, rec.pre_carrier and rec.pre_carrier or '', style8)
            sheet.write_merge(18, 18, 6, 8, "Place of Reciept:", style8)
            sheet.write_merge(18, 18, 9, 11, rec.pl_receipt and rec.pl_receipt or '', style8)

            sheet.write_merge(19, 19, 0, 2, 'Vessel/Flight No.:', style8)
            sheet.write_merge(19, 19, 3, 5, rec.flight_no and rec.flight_no or '', style8)
            sheet.write_merge(19, 19, 6, 8, "Port Of Loading:", style8)
            sheet.write_merge(19, 19, 9, 11, rec.port_loading and rec.port_loading or '', style8)

            sheet.write_merge(20, 20, 0, 2, 'Port of Discharge:', style8)
            sheet.write_merge(20, 20, 3, 5, rec.port_discharge and rec.port_discharge or '', style8)
            sheet.write_merge(20, 20, 6, 8, "Final Destination:", style8)
            sheet.write_merge(20, 20, 9, 11, rec.final_dest and rec.final_dest or '', style8)


            sheet.write_merge(21, 24, 0, 2, 'Marks & No.s/Container No.:' +'\n'+ (rec.container_no and str(rec.container_no) or '') +'\n'+
                (rec.container_no1 and str(rec.container_no1) or '') +'\n'+ (rec.container_no2 and str(rec.container_no2) or ''), style8) 
            sheet.write_merge(21, 24, 3, 5, 'No. & Kind of Pkgs.' +'\n'+ (rec.kind_pkg and str(rec.kind_pkg) or '') +'\n'+
                (rec.kind_pkg_unit and str(rec.kind_pkg_unit.name) or ''), style8) 
            sheet.write_merge(21, 24, 6, 11, "Commodity/Description & Services" +'\n'+ (rec.commodity_desc and str(rec.commodity_desc) or ''), style8) 
            
            sheet.write(25, 0, 'S.No.', style1)                           
            sheet.write_merge(25, 25, 1, 6, 'Item Description', style1)
            sheet.write_merge(25, 25, 7, 7, 'Quantity', style1) 
            sheet.write_merge(25, 25, 8, 8, 'Unit', style1)        
            sheet.write_merge(25, 25, 9, 9, 'Unit Price', style1)
            sheet.write_merge(25, 25,10,11, 'Total Amount', style1)
            n = 26; i = 1
            for product in custom_value['products']:
                sheet.write(n, 0, i, style5)  
                sheet.write_merge(n, n, 1, 6, product['product_id'], style6)      
                sheet.write_merge(n, n, 7, 7, str(int(product['product_qty'])), style0)
                sheet.write_merge(n, n, 8, 8, product['uom'], style0)
                sheet.write_merge(n, n, 9, 9, product['price_unit'], style0)
                sheet.write_merge(n, n,10,11, product['price_subtotal'], style0)                          
                n += 1; i += 1
            sheet.write_merge(n, n+7, 0, 6, 'Total Invoice Amount In Words ('+str(rec.currency_id.name) +') '+'\n'+
			rec.amount_to_text(rec.amount_total, rec.currency_id), style9)
            sheet.write_merge(n, n, 7, 7, [str(int(val['value'])) for val in self.get_qty()], style12)
            sheet.write_merge(n, n, 8, 8, [str(val['name']) for val in self.get_qty()], style9)
            sheet.write_merge(n, n, 9, 9, str(rec.currency_id.name), style9)
            sheet.write_merge(n, n, 10, 11, rec.amount_untaxed, style12)
            if rec.freight_charge > 0 :
            	sheet.write_merge(n+1, n+1, 7, 9, 'Freight & Insurance', style9)
            	sheet.write_merge(n+1, n+1, 10, 11, rec.freight_charge, style12)
                n += 1
            if rec.freight_charge == 0 :
            	sheet.write_merge(n+1, n+1, 7, 9, '', style10)
            	sheet.write_merge(n+1, n+1, 10, 11, '', style10)
                n += 1
            if rec.freight_only > 0 :
            	sheet.write_merge(n+1, n+1, 7, 9, 'Freight', style9)
            	sheet.write_merge(n+1, n+1, 10, 11, rec.freight_only, style12)
                n += 1
            if rec.freight_only == 0 :
            	sheet.write_merge(n+1, n+1, 7, 9, '', style10)
            	sheet.write_merge(n+1, n+1, 10, 11, '', style10)
                n += 1
            if rec.insurance_only > 0 :
            	sheet.write_merge(n+1, n+1, 7, 9, 'Insurance', style9)
            	sheet.write_merge(n+1, n+1, 10, 11, rec.insurance_only, style12)
                n += 1
            if rec.insurance_only == 0 :
            	sheet.write_merge(n+1, n+1, 7, 9, '', style10)
            	sheet.write_merge(n+1, n+1, 10, 11, '', style10)
                n += 1
            if rec.bank_charge > 0 :
            	sheet.write_merge(n+1, n+1, 7, 9, 'Banking & Handling', style9)
            	sheet.write_merge(n+1, n+1, 10, 11, rec.bank_charge, style12)
                n += 1
            if rec.bank_charge == 0 :
            	sheet.write_merge(n+1, n+1, 7, 9, '', style10)
            	sheet.write_merge(n+1, n+1, 10, 11, '', style10)
                n += 1
            if rec.ext_charge > 0 :
            	sheet.write_merge(n+1, n+1, 7, 9, 'Extra Charge', style9)
            	sheet.write_merge(n+1, n+1, 10, 11, rec.global_disc, style12)
                n += 1
            if rec.ext_charge == 0 :
            	sheet.write_merge(n+1, n+1, 7, 9, '', style10)
            	sheet.write_merge(n+1, n+1, 10, 11, '', style10)
                n += 1
            if rec.global_disc > 0 :
            	sheet.write_merge(n+1, n+1, 7, 9, 'Discount', style9)
            	sheet.write_merge(n+1, n+1, 10, 11, rec.global_disc, style12)
                n += 1
            if rec.global_disc == 0 :
            	sheet.write_merge(n+1, n+1, 7, 9, '', style10)
            	sheet.write_merge(n+1, n+1, 10, 11, '', style10)
                n += 1
            sheet.write_merge(n+1, n+1, 7, 9, 'Total '+str(rec.currency_id.name) + ','+ (rec.incoterms and str(rec.incoterms.name) or ''), style11)
            sheet.write_merge(n+1, n+1, 10, 11, '{0:.2f}'.format(rec.amount_total), style12)
            sheet.write_merge(n+2, n+4, 0, 5, 'IEC No.: '+str(rec.company_id.iec_no) + '\n'+ 'Total Gross Weight: '+str('%.3f'% round(rec.total_grwt)) +'\n'+ 'Total NET Weight: '+str('%.3f'% round(rec.total_ntwt)), style11)
            sheet.write_merge(n+2, n+4, 6, 11, 'For '+ str(rec.company_id.name) +'\n'+'\n'+'Authorised Signatory', style11)
            n += 1		
            #sheet.write_merge(n+1, n+1, 10, 11, 'Untaxed Amount', style7)
            #sheet.write(n+1, 27, custom_value['amount_untaxed'], style4)
            #sheet.write_merge(n+2, n+2, 10, 11, 'Taxes', style7)
            #sheet.write(n+2, 27, custom_value['amount_tax'], style4)
            #sheet.write_merge(n+3, n+3, 10, 11, 'Total', style7)
            #sheet.write(n+3, 27, custom_value['amount_total'], style4)
#CSV report
        datas = []
        for values in order:
            for value in values.invoice_line_ids:
                if value.product_id.seller_ids:
                    item = [
                            str(value.invoice_id.name or ''),
                            str(''),
                            str(''),                            
                            str(value.product_id.barcode or ''),
                            str(value.product_id.default_code or ''),
                            str(''),
                            str(value.quantity or ''),
                            str(value.product_id.seller_ids[0].product_code or ''),
                            str(value.partner_id.title or ''),
                            str(value.partner_id.name or ''),
                            str(value.partner_id.email or ''),
                            str(value.partner_id.phone or ''),
                            str(value.partner_id.mobile or ''),
                            str(value.partner_id.street or ''),
                            str(value.partner_id.street2 or ''),
                            str(value.partner_id.zip or ''),
                            str(value.partner_id.city or ''),
                            str(value.partner_id.country_id.name or ' '),                        
                            ] 
                    datas.append(item)    
            
        output = StringIO.StringIO()
        label = ';'.join(label_lists)               
        output.write(label)         
        output.write("\n")
                     
        for data in datas:       
            record = ';'.join(data)
            output.write(record)
            output.write("\n")
        data = base64.encodestring(output.getvalue())

        if platform.system() == 'Linux':
            filename = ('/home/odoo/workspace/odoo10/odoo10/CI Report-' + str(datetime.today().date()) + '.xls')
            #filename2 = ('/usr/lib/python2.7/dist-packages/odoo/addons/CI Report-' + str(datetime.today().date()) + '.csv')
        else:
            filename = ('/home/odoo/workspace/odoo10/odoo10/CI Report-' + str(datetime.today().date()) + '.xls')
            #filename2 = ('/usr/lib/python2.7/dist-packages/odoo/addons/CI Report-' + str(datetime.today().date()) + '.csv')

        filename = filename.split('/')[2]
        #filename2 = filename2.split('/')[2]
        workbook.save('/home/odoo/workspace/odoo10/odoo10/CI Report.xls')
        fp = open('/home/odoo/workspace/odoo10/odoo10/CI Report.xls', "rb")
        file_data = fp.read()
        out = base64.encodestring(file_data)                                                 
                       
# Files actions         
        attach_vals = {
                'invoice_data': 'Commercial Invoice-'+str(rec.partner_id.name)+'.xls',
                'file_name': out,
                #'invoice_work':filename2,
                'file_names':data,
            } 
            
        act_id = self.env['invoice.report.out'].create(attach_vals)
        fp.close()
        return {
        'type': 'ir.actions.act_window',
        'res_model': 'invoice.report.out',
        'res_id': act_id.id,
        'view_type': 'form',
        'view_mode': 'form',
        'context': self.env.context,
        'target': 'new',
        }
                          
        

 





























