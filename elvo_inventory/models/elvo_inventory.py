from odoo import models, fields, api

class Inventory(models.Model):
    _inherit = "stock.inventory"

    pic1 = fields.Many2one("res.users", string="PIC 1")
    pic2 = fields.Many2one("res.users", string="PIC 2")

class StockPicking(models.Model):
    _inherit = "stock.picking"

    resi_kirim = fields.Char(string="Resi Kirim")
