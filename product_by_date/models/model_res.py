from odoo import models, fields, api
import logging
import requests
_logger = logging.getLogger(__name__)
import json
import io
from odoo.exceptions import UserError
from odoo.tools.translate import _

class ResPartPortal(models.Model):
    _inherit= "res.partner"

    reference = fields.Char(string='Referencia', required=False)
