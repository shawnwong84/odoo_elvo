from odoo import fields, models, api, _

class MasterMarketplace(models.Model):
    _name = 'master.marketplace'
    _description = 'Marketplace'

    name = fields.Char(string="Marketplace Name", required=True)

class CustomerMarketplace(models.Model):
    _name = 'history.order'
    _description = 'Customer Marketplace'

    marketplace_id = fields.Many2one('master.marketplace', string="Marketplace")
    order_id = fields.Integer(string="Order ID")
    customer_name = fields.Char(string="Customer Name")
    customer_receipt = fields.Char(string="Customer Receipt")
    phone_marketplace = fields.Char(string="Phone Marketplace")
    phone_receipt = fields.Char(string="Phone Receipt")
    email_marketplace = fields.Char(string="Email Marketplace")
    address_marketplace = fields.Char(string="Address Marketplace")

class Partner(models.Model):
    _inherit = 'res.partner'

    marketplace_ids = fields.One2many('history.order', 'order_id', string="Marketplace")