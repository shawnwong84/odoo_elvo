from odoo import models, fields, api, _

class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    shopee = fields.Float(string='Shopee', digits=(16, 2))
    tokped = fields.Float(string='Tokopedia', digits=(16, 2))
    lazada = fields.Float(string='Lazada', digits=(16, 2))
    tiktok = fields.Float(string='Tiktok', digits=(16, 2))
    order_online = fields.Float(string='Order Online', digits=(16, 2))