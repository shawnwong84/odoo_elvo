from odoo import models, fields, api

class PurchaseOrderNote(models.Model):
    _name = 'purchase.order.note'
    _description = 'Elvo Purchase Order Notes'

    name = fields.Char(string="Notes")