import io
from odoo import http, fields
from odoo.http import request
import base64
import logging
_logger = logging.getLogger(__name__)
from datetime import datetime, timedelta

import pandas as pd
from io import BytesIO
import re
import werkzeug.utils
import pytz
import xlsxwriter

import openpyxl

class ReportExcelProdController(http.Controller):

    @http.route('/download/excel_file_process', type='http', auth='public', website=True)
    def download_excel(self, id=None, **kwargs):

        _logger.info("SE EJECUTO GET PRODUCTS")
        
        data_to_excel = []
        
        if id:
        
            informe_data = request.env['excel.report.product'].sudo().search([('id','=', id)])
            
            if informe_data:
                
                date_start_product = fields.Datetime.to_string(informe_data.date_start.replace(hour=18, minute=0, second=0, microsecond=0)) 
                
                date_end_product = fields.Datetime.to_string(informe_data.date_end.replace(hour=18, minute=0, second=0, microsecond=0)) 

                #Agregar ('company_id', '=', informe_data.company_id) al filtro de busqueda de productos
                products_start = request.env['product.product'].sudo().with_context(to_date=date_start_product).search([('type', '=', 'product')]) 

                #Agregar ('company_id', '=', informe_data.company_id) al filtro de busqueda de productoss
                products_end = request.env['product.product'].sudo().with_context(to_date=date_end_product).search([('type', '=', 'product')]) 

                products_start[0].qty_available  
                
                output = io.BytesIO()
                workbook = xlsxwriter.Workbook(output)
                worksheet = workbook.add_worksheet()
                worksheet.write(0, 0, 'Producto')
                worksheet.write(0, 1, 'Referencia interna')
                worksheet.write(0, 2, 'Cantidad en fecha de inicio')
                worksheet.write(0, 3, 'Cantidad en fecha final')
                worksheet.write(0, 4, 'Ventas del periodo')
                worksheet.write(0, 5, 'Diferencia')
                
                fila_inicio = 1
                for product in products_start:
                    qty_start = product.qty_available
                    data_to_excel.append({
                        'id': product.id,
                        'name_product': product.name,
                        'reference': product.default_code,
                        'qty_start': qty_start
                    })
                   
                
                #obtener cantidad por fecha final
                
                #for product_fin in products_end:
                    #product_end = product.qty_available
                    #for rec in data_to_excel:
                       # if rec['id'] == product_fin.id:
                          #  data_to_excel
                   
                    
                #obtener las ventas por semana 
                
                
                #sale_order_lines = request.env['sale.order.line'].sudo().search([
                #    ('product_id', '=', product_id),
                #    ('create_date', '>=', start_date),
                 #   ('create_date', '<', end_date)
                #])
                
                for data in data_to_excel:
                    qty_start = data['qty_start']

                    worksheet.write(fila_inicio, 0, data['name_product'])
                    worksheet.write(fila_inicio, 1, data['reference'])
                    worksheet.write(fila_inicio, 2, qty_start)
                    fila_inicio += 1

                workbook.close()
                
                response = request.make_response(output.getvalue())
                response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                response.headers['Content-Disposition'] = f'attachment; filename=prueba.xlsx'

                return response

