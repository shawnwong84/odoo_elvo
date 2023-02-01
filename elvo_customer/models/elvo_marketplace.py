from odoo import fields, models, api, _
from odoo.exceptions import UserError
import requests
import json
from datetime import datetime
import time
import hashlib
import calendar
import hmac
import lazop_sdk as lazop


class MasterMarketplace(models.Model):
    _name = 'master.marketplace'
    _description = 'Marketplace'

    name = fields.Char(string="Marketplace Name", required=True)

    def test_api(self):
        client = lazop.LazopClient('https://auth.lazada.com/rest', '115530', '748b3104-2892-47c9-3d91-1469e1d48874')
        request = lazop.LazopRequest('/seller/get', 'GET')
        response = client.execute(request, '92c5fff4cac74b7d80a7c7206f55532d')
        print(response.type)
        print(response.body)
        # request = lazop.LazopRequest('/auth/token/create')
        # request.add_api_param('code', '0_100132_2DL4DV3jcU1UOT7WGI1A4rY91')
        # request.add_api_param('uuid', 'This field is currently invalid,  do not use this field please')
        # response = client.execute(request)
        # print(response.type)
        # print(response.body)
        # client = lazop.LazopClient("https://auth.lazada.com/rest", "115530", "pvErlXpt2WsdjkrrF7zqi5xHWGvde3rY")
        # request = lazop.LazopRequest('/auth/token/create')
        # request.add_api_param('code', '0_100132_2DL4DV3jcU1UOT7WGI1A4rY91')
        # request.add_api_param('uuid', 'This field is currently invalid,  do not use this field please')
        # response = client.execute(request)
        # print(response.type)
        # print(response.body)
        # a = self.sign("115530", "pvErlXpt2WsdjkrrF7zqi5xHWGvde3rY")
        raise UserError(str(response.body))

    # def convert_time(self):
    #     # get current date and time
    #     current_time = datetime.now()
    #     # convert datetime object to timestamp
    #     timestamp = time.mktime(current_time.timetuple())
    #     # convert timestamp to milliseconds
    #     timestamp = int(timestamp * 1000)
    #     return timestamp
    #
    def sign(self, secret, api, parameters):
        # ===========================================================================
        # @param secret
        # @param parameters
        # ===========================================================================
        sort_dict = sorted(parameters)

        parameters_str = "%s%s" % (api,
                                   str().join('%s%s' % (key, parameters[key]) for key in sort_dict))

        h = hmac.new(secret.encode(encoding="utf-8"), parameters_str.encode(encoding="utf-8"), digestmod=hashlib.sha256)

        return h.hexdigest().upper()
    def generate_sign_method(self, app_key, app_secret):
        # Concatenate app_key and app_secret
        data = app_key + app_secret
        # Create SHA-256 hash
        sign_method = hashlib.sha256(data.encode()).hexdigest()
        return sign_method
    #
    # def generate_sign_method(self, app_key, app_secret):
    #     # Concatenate app_key and app_secret
    #     data = app_key + app_secret
    #     # Create SHA-256 hash
    #     sign_method = hashlib.sha256(data.encode()).hexdigest()
    #     return sign_method
    #
    # def sign(self, secret, api, parameters):
    #     # ===========================================================================
    #     # @param secret
    #     # @param parameters
    #     # ===========================================================================
    #     sort_dict = sorted(parameters)
    #
    #     parameters_str = "%s%s" % (api,
    #                                str().join('%s%s' % (key, parameters[key]) for key in sort_dict))
    #
    #     h = hmac.new(secret.encode(encoding="utf-8"), parameters_str.encode(encoding="utf-8"), digestmod=hashlib.sha256)
    #
    #     return h.hexdigest().upper()
    #
    # def test_api(self):
    #     app_key = "115530"
    #     app_secret = "pvErlXpt2WsdjkrrF7zqi5xHWGvde3rY"
    #     code = "your_authorization_code"
    #     url = "https://auth.lazada.com/rest/auth/token/create"
    #     sign_method = self.generate_sign_method(app_key, app_secret)
    #     timestamp = self.convert_time()
    #     sign = self.sign(app_secret, app_key)
    #     data = {
    #         "code": code,
    #         "app_key": app_key,
    #         "app_secret": app_secret,
    #         'timestamp': timestamp,
    #         'sign_method': sign_method,
    #         'sign': sign,
    #
    #     }
    #     headers = {
    #         "Content-Type": "application/json"
    #     }
    #     response = requests.post(url, json=data, headers=headers)
    #     raise UserError(response.text)


class CustomerMarketplace(models.Model):
    _name = 'history.order'
    _description = 'Customer Marketplace'

    marketplace_id = fields.Many2one('master.marketplace', string="Marketplace Name")
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
