from odoo import fields, models, api, _

class CustomerMarketplace(models.Model):
    _name = 'history.order'
    _description = 'Customer Marketplace'

    marketplace_id = fields.Many2one('master.marketplace', string="Marketplace Name")
    partner_id = fields.Many2one('res.partner', string="Customer")
    order_id = fields.Integer(string="Order ID")
    customer_name = fields.Char(string="Customer Name")
    customer_receipt = fields.Char(string="Customer Receipt")
    phone_marketplace = fields.Char(string="Phone Marketplace")
    phone_receipt = fields.Char(string="Phone Receipt")
    email_marketplace = fields.Char(string="Email Marketplace")
    address_marketplace = fields.Char(string="Address Marketplace")


class Partner(models.Model):
    _inherit = 'res.partner'

    def open_history_order(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'History Order',
            'view_mode': 'tree',
            'res_model': 'history.order',
            # 'domain': [('partner_id', '=', self.id)],
            'context': "{'create': False}",
            'search_default_partner_id': self.id,
        }

    marketplace_ids = fields.One2many('history.order', 'order_id', string="Marketplace")
