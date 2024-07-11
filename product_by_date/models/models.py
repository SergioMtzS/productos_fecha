import io

from odoo.http import request
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import hashlib
import logging
_logger = logging.getLogger(__name__)
import pandas as pd
from io import BytesIO
import werkzeug.utils
import pytz
import xlsxwriter

class ExcelReportProd(models.Model):

    _name = 'excel.report.product'
    _description = 'Informe en excel'
    
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    
    date_start = fields.Datetime(string='Fecha inicial', required= True)
    
    date_end = fields.Datetime(string='fecha Final', required= True)

    def _automated_get_products_by_date(self, date_start, date_end):
        companies = self.env['res.company'].search()
        for company in companies:
            self.get_products_by_date(company.id, date_start, date_end)

    def get_products_by_date(self):
        
                
        return {
            'type': 'ir.actions.act_url',
            'url': '/download/excel_file_process?id='+ str(self.id),
            'target': 'self',
        }
