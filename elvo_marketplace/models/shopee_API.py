from odoo import fields, models, api, _
from odoo.exceptions import UserError
import hmac
import json
import time
import requests
import hashlib
import datetime

class MasterMarketplace(models.Model):
    _inherit = 'master.marketplace'

    shopee_code = fields.Char(string="Shopee Code")
    shopee_partner_id = fields.Integer(string="Shopee Partner ID")
    shopee_shop_id = fields.Integer(string="Shopee Shop ID")
    shopee_partner_key = fields.Char(string="Shopee Partner Key")

    def shopee_get_code(self):
        timest = int(time.time())
        # host = "https://partner.test-stable.shopeemobile.com"
        host = 'https://partner.shopeemobile.com'
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
        timest = int(time.time())
        host = "https://partner.shopeemobile.com"
        path = "/api/v2/auth/token/get"
        body = {"code": self.shopee_code, "shop_id": self.shopee_shop_id, "partner_id": self.shopee_partner_id}
        tmp_base_string = "%s%s%s" % (self.shopee_partner_id, path, timest)
        base_string = tmp_base_string.encode()
        partner_key = self.shopee_partner_key.encode()
        sign = hmac.new(partner_key, base_string, hashlib.sha256).hexdigest()
        url = host + path + "?partner_id=%s&timestamp=%s&sign=%s" % (self.shopee_partner_id, timest, sign)
        # print(url)
        headers = {"Content-Type": "application/json"}
        resp = requests.post(url, json=body, headers=headers)
        ret = json.loads(resp.content)
        if resp.json()['error']:
            raise UserError("Error: Update Code and Try Again")
        access_token = ret.get("access_token")
        new_refresh_token = ret.get("refresh_token")
        self.token = access_token
        self.refresh_token = new_refresh_token

    def shopee_refresh_token(self):
        url = "https://partner.shopeemobile.com/api/v2/auth/access_token/get"
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

    def generate_signature(self, partner_id, api_path, timestamp, access_token, shop_id, partner_key):
        params_string = f"partner_id{partner_id}shop_id{shop_id}access_token{access_token}timestamp{timestamp}"
        params_string += api_path
        hashed = hmac.new(partner_key.encode(), params_string.encode(), hashlib.sha256)
        raise UserError(hashed.hexdigest())
        return hashed.hexdigest()

    def shopee_get_order_list(self):
        path = "api/v2/order/get_order_list"
        partner_id = self.shopee_partner_id
        shop_id = self.shopee_shop_id
        access_token = self.token
        time_to = datetime.datetime.now()
        time_from = time_to - datetime.timedelta(days=3)
        timestamp = int(time_to.timestamp())
        # params = {
        #     "partner_id": partner_id,
        #     "timestamp": timestamp,
        #     "access_token": access_token,
        #     "shop_id": shop_id,
        # }
        # sorted_params = "".join([f"{k}{v}" for k, v in sorted(params.items())])
        # message = sorted_params.encode("utf-8")
        # sign = hmac.new(self.shopee_partner_key.encode("utf-8"), message, hashlib.sha256).hexdigest()
        sign = self.generate_signature(partner_id, path, timestamp, access_token, shop_id, self.shopee_partner_key)
        url = f"https://partner.shopeemobile.com/{path}?timestamp={timestamp}&shop_id={shop_id}&order_status=READY_TO_SHIP&partner_id={partner_id}&access_token={access_token}&page_size=20&response_optional_fields=order_status&time_range_field=create_time&time_from={time_from}&time_to={time_to}&sign={sign}&cursor="

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # process the data here
        else:
            print("Request failed with status code:", response.text)

