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
    username = fields.Char(string="Username")
    password = fields.Char(string="Password")
    email = fields.Char(string="Email")
    token = fields.Char(string="Token")
    refresh_token = fields.Char(string="Refresh Token")
    shopee_code = fields.Char(string="Shopee Code")

    def shopee_auth(self):
        timest = int(time.time())
        host = "https://partner.test-stable.shopeemobile.com"
        path = "/api/v2/shop/auth_partner"
        redirect_url = "https://github.com/"
        partner_id = 1023606
        tmp = "7a4e7562417570427842416745516b796547476f72417a6a706e586778645961"
        partner_key = tmp.encode()
        tmp_base_string = "%s%s%s" % (partner_id, path, timest)
        base_string = tmp_base_string.encode()
        sign = hmac.new(partner_key, base_string, hashlib.sha256).hexdigest()
        url = host + path + "?partner_id=%s&timestamp=%s&sign=%s&redirect=%s" % (partner_id, timest, sign, redirect_url)
        print(url)
        raise UserError(url)

    def shopee_get_token(self):
        url = "https://partner.test-stable.shopeemobile.com/api/v2/auth/token/get"

        payload = json.dumps({
            "code": "41416e4f49744c57634c45724a595266",
            "partner_id": 1023606,
            "shop_id": 75058
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

    def shopee_refresh_token(self):
        url = "https://partner.test-stable.shopeemobile.com/api/v2/auth/access_token/get"

        payload = json.dumps({
            "refresh_token": "586d624f614877737072656c47514779",
            "code": "4943475345527a4d784e504b51484b76",
            "partner_id": 1023606,
            "shop_id": 75058
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
