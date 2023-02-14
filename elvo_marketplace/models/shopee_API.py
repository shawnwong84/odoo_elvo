from odoo import fields, models, api, _
from odoo.exceptions import UserError
import hmac
import json
import time
import requests
import hashlib

class MasterMarketplace(models.Model):
    _inherit = 'master.marketplace'

    shopee_code = fields.Char(string="Shopee Code")
    shopee_partner_id = fields.Integer(string="Shopee Partner ID")
    shopee_shop_id = fields.Integer(string="Shopee Shop ID")
    shopee_partner_key = fields.Char(string="Shopee Partner Key")

    def shopee_get_code(self):
        timest = int(time.time())
        host = "https://partner.test-stable.shopeemobile.com"
        path = "/api/v2/shop/auth_partner"
        redirect_url = "https://github.com/"
        partner_id = self.shopee_partner_id
        tmp = self.shopee_partner_key
        partner_key = tmp.encode()
        tmp_base_string = "%s%s%s" % (partner_id, path, timest)
        base_string = tmp_base_string.encode()
        sign = hmac.new(partner_key, base_string, hashlib.sha256).hexdigest()
        url = host + path + "?partner_id=%s&timestamp=%s&sign=%s&redirect=%s" % (partner_id, timest, sign, redirect_url)
        raise UserError(url)

    def shopee_get_token(self):
        url = "https://partner.test-stable.shopeemobile.com/api/v2/auth/token/get"
        payload = json.dumps({
            "code": self.shopee_code,
            "partner_id": self.shopee_partner_id,
            "shop_id": self.shopee_shop_id
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.json()['error']:
            raise UserError("Error: Update Code and Try Again")
        self.token = response.json()['access_token']
        self.refresh_token = response.json()['refresh_token']

    def shopee_refresh_token(self):
        url = "https://partner.test-stable.shopeemobile.com/api/v2/auth/access_token/get"
        payload = json.dumps({
            "refresh_token": self.refresh_token,
            "code": self.shopee_code,
            "partner_id": self.shopee_partner_id,
            "shop_id": self.shopee_shop_id
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        self.token = response.json()['access_token']
        self.refresh_token = response.json()['refresh_token']