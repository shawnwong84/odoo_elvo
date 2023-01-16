from odoo import models, fields, api


class SupplierInfo(models.Model):
    _inherit = 'product.supplierinfo'

    price_latest = fields.Float(string='Latest Price')