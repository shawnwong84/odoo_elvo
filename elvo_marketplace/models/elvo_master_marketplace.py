from odoo import fields, models, api, _
from odoo.exceptions import UserError
import hmac
import json
import time
import requests
import hashlib

class MasterMarketplace(models.Model):
    _name = 'master.marketplace'
    _description = 'Marketplace'

    name = fields.Char(string="Name", required=True)
    marketplace = fields.Selection([
        ('shopee', 'Shopee'),
        ('tokopedia', 'Tokopedia'),
        ('lazada', 'Lazada'),
        ('tiktok', 'Tiktok'),
        ('order_online', 'Order Online'),
    ], string="Marketplace", required=True)
    username = fields.Char(string="Username")
    password = fields.Char(string="Password")
    email = fields.Char(string="Email")
    token = fields.Char(string="Token")
    refresh_token = fields.Char(string="Refresh Token")