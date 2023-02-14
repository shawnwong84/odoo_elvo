from odoo import fields, models, api, _
from odoo.exceptions import UserError
import hmac
import json
import time
import requests
import hashlib


class MasterMarketplace(models.Model):
    _inherit = 'master.marketplace'

    tiktok_app_key = fields.Char(string="Tiktok App Key")
    tiktok_auth_code = fields.Char(string="Tiktok Auth Code")
    tiktok_app_secret = fields.Char(string="Tiktok App Secret")

    def tiktok_get_code(self):
        url = "https://auth.tiktok-shops.com/api/v2/token/get?app_key=" + self.tiktok_app_key + "&auth_code=" + self.tiktok_auth_code +"&app_secret=" + self.tiktok_app_secret + "&grant_type=authorized_code"
        payload = {}
        files = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload, files=files)
        if 'data' not in response.json():
            raise UserError("Error: Update Code and Try Again")
        self.token = response.json()['data']['access_token']
        self.refresh_token = response.json()['data']['refresh_token']

    def get_tiktok_code(self):
        raise UserError("https://services.tiktokshop.com/open/authorize?service_id=7189844839901497093")
