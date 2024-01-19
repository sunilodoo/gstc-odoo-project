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


class SaleOrderOut(models.Model):        
    _name = 'sale.order.out'
    _description = 'Sale Order Report'
    
    sale_data = fields.Char('Name', size=256)
    file_name = fields.Binary('Order Excel Report', readonly=True)
    sale_work = fields.Char('Name', size=256)
    file_names = fields.Binary('Order CSV Report', readonly=True)
    
   
class OrderWizards(models.Model):        
    _name = 'order.reports'
    _description = 'Order wizard'
    
    @api.multi
    def get_order(self):
		order = self.env['account.invoice'].browse(self._context.get('active_ids', list()))
		for inv in order:
			so = self.env['sale.order'].search([('name','=',inv.origin)])
			result = []
			result.append({'mode_of_ship': so.carrier_id.name, 'delivery_term': so.incoterms.name})
			print"---------result----=====----result---",result
		return result

    @api.multi
    def get_qty(self):
		result = []
		c = defaultdict(int)
		order = self.env['account.invoice'].browse(self._context.get('active_ids', list()))
		for inv in order:
			for line in inv.order_line_ids:
				if line.uom_id:
					print"---------line.uom_id.name===",line.uom_id.name
					result.append({'name':line.uom_id.name, 'value': line.quantity})
		print"---------result----=====----get_qty---",result
		for d in result:
			c[d['name']] += d['value']
		return [{'name': name, 'value': val} for name, val in c.items()]
               
    @api.multi
    def action_order_report(self):          
#XLS report         
        custom_value = {}
        label_lists=['PO','POR','CLIENTREF','BARCODE','DEFAULTCODE','NAME','QTY','VENDORPRODUCTCODE','TITLE', 'PARTNERNAME', 'EMAIL', 'PHONE', 'MOBILE', 'STREET', 'STREET2', 'ZIP', 'CITY', 'COUNTRY']                    
        orders = self.env['sale.order'].browse(self._context.get('active_ids', list()))      
        workbook = xlwt.Workbook()                      
        for rec in orders:              
            order = []                                                          
            for line in rec.order_line:                              
                product = {}                                                                       
                product ['product_id'] = line.product_id.name                                                                            
                product ['product_qty'] = line.product_uom_qty                           
                product ['uom'] = line.product_uom.name                          
                product ['price_unit'] = '{0:.4f}'.format(line.price_unit)                      
                product ['price_subtotal'] = '{0:.2f}'.format(line.price_subtotal)                       
                order.append(product)
                                                                                           
            custom_value['products'] = order               
            custom_value ['partner_id'] = rec.partner_id.name
            custom_value ['partner_ref'] = ''
            custom_value ['payment_term_id'] = rec.payment_term_id.name
            custom_value ['date_order'] = rec.date_order
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
            style13 = xlwt.easyxf('font: name Times New Roman, bold True, height 300;align: horiz center;borders: bottom_color black, top_color black, right_color black, left_color black,left thin, right thin, bottom thin, top thin;', num_format_str='#,##0.00')
                          
            sheet = workbook.add_sheet(rec.name or 'Sale Order',cell_overwrite_ok=True)
            sheet.write_merge(0, 1, 0, 11, 'Sale Order', style2)
            
            sheet.write_merge(2, 2, 0, 5, 'EXPORTER', style9)
            sheet.write_merge(3, 8, 0, 5, rec.company_id.partner_id.name +'\n'+ rec.company_id.partner_id.street +' '+ 
                rec.company_id.partner_id.street2 +'\n'+ rec.company_id.partner_id.city +' '+ rec.company_id.partner_id.zip +', '+
                rec.company_id.partner_id.country_id.name +'\n'+
                (rec.company_id.partner_id.gstn and 'GSTIN: '+str(rec.company_id.partner_id.gstn) or '') +'\n'+ 
                (rec.company_id.partner_id.phone and 'WhatsApp No.: +91 8800010925') +'\n'+ 
                (rec.company_id.partner_id.email and 'Email: '+str(rec.company_id.partner_id.email) or ''), style8)

            
            sheet.write_merge(2, 2, 6, 11, 'Our Bankers', style9)
            sheet.write_merge(3, 8, 6, 11, 'Indian Overseas Bank, 14-15 Farm bhawan' +'\n'+ 'Nehru Place- 19, New Delhi' +'\n'+ 'Swift code: IOBAINBB 543' +'\n'+
                'A/c name: GST CORPORATION LIMITED' +'\n'+ 
                'Account No.: 054302000051599' + '\n'+'\n', style8)
            
            if rec.partner_id == rec.consignee:
            	sheet.write_merge(9, 10, 0, 5, 'Buyer and Consignee Address', style9)
            if rec.partner_id != rec.consignee:
            	sheet.write_merge(9, 10, 0, 5, 'Buyer Address', style9)
            sheet.write_merge(11, 17, 0, 5, rec.partner_id.name +'\n'+ str(rec.partner_id.street) +'\n'+ 
                str(rec.partner_id.street2) +'\n'+ str(rec.partner_id.city) +' '+ 
                (rec.partner_id.zip and str(rec.partner_id.zip) or '') +' '+ str(rec.partner_id.country_id.name) +'\n'+ 
                (rec.partner_id.email and 'Email: '+str(rec.partner_id.email) or '') +'\n'+ 
                (rec.partner_id.phone and 'Phone: '+str(rec.partner_id.phone) or '') +'\n'+ 
                (rec.partner_id.fax and 'Fax: '+str(rec.partner_id.fax) or '') , style8)
            
            if rec.is_consignee and rec.consignee and (rec.partner_id == rec.consignee):
            	sheet.write_merge(9, 10, 6, 11, 'Consignee(if other than Buyer)', style9)
            	sheet.write_merge(11, 17, 6, 11, rec.partner_id.name +'\n'+ str(rec.partner_id.street) +'\n'+ 
		            str(rec.partner_id.street2) +'\n'+ str(rec.partner_id.city) +' '+ 
		            (rec.partner_id.zip and str(rec.partner_id.zip) or '') +' '+ str(rec.partner_id.country_id.name) +'\n'+ 
		            (rec.partner_id.email and 'Email: '+str(rec.partner_id.email) or '') +'\n'+ 
		            (rec.partner_id.phone and 'Phone: '+str(rec.partner_id.phone) or '') +'\n'+ 
		            (rec.partner_id.fax and 'Fax: '+str(rec.partner_id.fax) or '') , style8)
                
            if not rec.consignee:
            	sheet.write_merge(9, 10, 6, 11, 'Consignee(if other than Buyer)', style9)
            	sheet.write_merge(11, 17, 6, 11, rec.partner_id.name +'\n'+ str(rec.partner_id.street) +'\n'+ 
		            str(rec.partner_id.street2) +'\n'+ str(rec.partner_id.city) +' '+ 
		            (rec.partner_id.zip and str(rec.partner_id.zip) or '') +' '+ str(rec.partner_id.country_id.name) +'\n'+ 
		            (rec.partner_id.email and 'Email: '+str(rec.partner_id.email) or '') +'\n'+ 
		            (rec.partner_id.phone and 'Phone: '+str(rec.partner_id.phone) or '') +'\n'+ 
		            (rec.partner_id.fax and 'Fax: '+str(rec.partner_id.fax) or '') , style8)
            if rec.consignee and rec.partner_id != rec.consignee:
            	sheet.write_merge(9, 10, 6, 11, 'Consignee Address', style9)
            	sheet.write_merge(11, 17, 6, 11, rec.consignee.name +'\n'+ str(rec.consignee.street) +'\n'+ 
		            str(rec.consignee.street2) +'\n'+ str(rec.consignee.city) +' '+ 
		            (rec.consignee.zip and str(rec.consignee.zip) or '') +' '+ str(rec.consignee.country_id.name) +'\n'+ 
		            (rec.consignee.email and 'Email: '+str(rec.consignee.email) or '') +'\n'+ 
		            (rec.consignee.phone and 'Phone: '+str(rec.consignee.phone) or '') +'\n'+ 
		            (rec.consignee.fax and 'Fax: '+str(rec.consignee.fax) or '') , style8)
            sheet.write_merge(18, 18, 0, 2, 'Buyer Reference:', style8)
            sheet.write_merge(18, 18, 3, 5, rec.buyer_ref and rec.buyer_ref or '', style8)
            sheet.write_merge(18, 18, 6, 8, "Date:", style8)
            sheet.write_merge(18, 18, 9, 11, rec.date_order and datetime.strptime(rec.date_order, '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y') or '', style8)

            sheet.write_merge(19, 19, 0, 2, 'Mode of Shipment:', style8)
            sheet.write_merge(19, 19, 3, 5, rec.carrier_id and rec.carrier_id.name or '', style8)
            sheet.write_merge(19, 19, 6, 8, "Deliver Period:", style8)
            sheet.write_merge(19, 19, 9, 11, rec.delivery_time and rec.delivery_time.name or '', style8)

            sheet.write_merge(20, 20, 0, 2, 'Payment Terms:', style8)
            sheet.write_merge(20, 20, 3, 5, rec.payment_term_id and rec.payment_term_id.name or '', style8)
            sheet.write_merge(20, 20, 6, 8, "Incoterms:", style8)
            sheet.write_merge(20, 20, 9, 11, rec.incoterms and rec.incoterms.name or '', style8)
            sheet.write_merge(21, 21, 0, 2, 'Validity of PI:', style8) 
            sheet.write_merge(21, 21, 3, 5, rec.validity_date and rec.validity_date or '', style8)
            sheet.write_merge(21, 21, 6, 11, '', style8) 
            
            sheet.write_merge(22, 23, 0, 11, 'PROFORMA No. ' + str(rec.name) +' Date '+ datetime.strptime(rec.date_order, '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y') + ' '+(rec.revision_date and 'Revised Date '+datetime.strptime(rec.revision_date, '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y') or ''), style13) 
            
            sheet.write(24, 0, 'S.No.', style1)                           
            sheet.write_merge(24, 24, 1, 6, 'Item Description', style1)
            sheet.write_merge(24, 24, 7, 7, 'Quantity', style1) 
            sheet.write_merge(24, 24, 8, 8, 'Unit', style1)        
            sheet.write_merge(24, 24, 9, 9, 'Unit Price', style1)
            sheet.write_merge(24, 24,10,11, 'Total Amount', style1)
            n = 25; i = 1
            for product in custom_value['products']:
                sheet.write(n, 0, i, style5)  
                sheet.write_merge(n, n, 1, 6, product['product_id'], style6)      
                sheet.write_merge(n, n, 7, 7, str(int(product['product_qty'])), style0)
                sheet.write_merge(n, n, 8, 8, product['uom'], style0)
                sheet.write_merge(n, n, 9, 9, product['price_unit'], style0)
                sheet.write_merge(n, n,10,11, product['price_subtotal'], style0)                          
                n += 1; i += 1
            sheet.write_merge(n, n+7, 0, 6, 'Total Order Amount In Words '+str(rec.currency_id.name)+'\n'+
			rec.amount_to_text(rec.amount_total, rec.currency_id), style9)
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
            if rec.ext_chrgs > 0 :
            	sheet.write_merge(n+1, n+1, 7, 9, rec.chrgs_inf, style9)
            	sheet.write_merge(n+1, n+1, 10, 11, rec.ext_chrgs, style12)
                n += 1
            if rec.ext_chrgs == 0 :
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
            sheet.write_merge(n+1, n+1, 7, 9, 'Total '+str(rec.pricelist_id.currency_id.name) + ', '+ (rec.incoterms and str(rec.incoterms.name) or ''), style11)
            sheet.write_merge(n+1, n+1, 10, 11, '{0:.2f}'.format(rec.full_total), style12)
            sheet.write_merge(n+2, n+4, 0, 5, 'Remarks '+ '\n'+(rec.remarks and str(rec.remarks) or ''), style11)
            sheet.write_merge(n+2, n+4, 6, 11, 'For '+ str(rec.company_id.name) +'\n'+'\n'+'Authorised Signatory', style11)
            n += 1	
        datas = []
        for values in orders:
            for value in values.order_line:
                if value.product_id.seller_ids:
                    item = [
                            str(value.name or ''),
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
            filename = ('/home/odoo/workspace/odoo10/odoo10/PI Report-' + str(datetime.today().date()) + '.xls')
            #filename2 = ('order/PI Report-' + str(datetime.today().date()) + '.csv')
        else:
            filename = ('/home/odoo/workspace/odoo10/odoo10/CI Report-' + str(datetime.today().date()) + '.xls')
            #filename2 = ('Order Report-' + str(datetime.today().date()) + '.csv')

        print"-----------filename----",filename
        filename = filename.split('/')[1]
        #filename2 = filename2.split('/')[1]
        workbook.save('/home/odoo/workspace/odoo10/odoo10/PI Report.xls')
        fp = open('/home/odoo/workspace/odoo10/odoo10/PI Report.xls', "rb")
        file_data = fp.read()
        out = base64.encodestring(file_data)                                                 
                       
# Files actions         
        attach_vals = {
                'sale_data': 'PI -'+str(rec.partner_id.name)+'.xls',
                'file_name': out,
                #'sale_work':filename2,
                'file_names':data,
            } 
            
        act_id = self.env['sale.order.out'].create(attach_vals)
        fp.close()
        return {
        'type': 'ir.actions.act_window',
        'res_model': 'sale.order.out',
        'res_id': act_id.id,
        'view_type': 'form',
        'view_mode': 'form',
        'context': self.env.context,
        'target': 'new',
        }
                          
        

 





























