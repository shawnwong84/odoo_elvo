from odoo import models, fields, api

class Inventory(models.Model):
    _inherit = "stock.inventory"

    pic1 = fields.Many2one("res.partner", string="PIC 1")
    pic2 = fields.Many2one("res.partner", string="PIC 2")