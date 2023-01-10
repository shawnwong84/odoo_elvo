from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('to_approve_manager', 'To Approve Manager Finance'),
        ('to_approve_finance', 'To Approve Finance'),
        ('to_approve_bod', 'To Approve BOD'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)
    po_notes = fields.Selection([
        ('note1', 'MOHON KONFIRMASI SETELAH MENERIMA PO.'),
        ('note2', 'MOHON MENCANTUMKAN NOMOR PO PADA SURAT JALAN.'),
        ('note3', 'ALAMAT KIRIM BARANG SESUAI ALAMAT PENGIRIMAN DI PO.'),
        ('note4', 'FRANCO GUDANG ALAMAT PENGIRIMAN.')
    ], string="Notes")
    tolerance = fields.Char(string="Tolerance")
    reason = fields.Char(string="Reason")
    hide_confirm_order = fields.Boolean(compute="_compute_hide_button", default=True)
    hide_approve_manager = fields.Boolean(compute="_compute_hide_button", default=True)
    hide_approve_finance = fields.Boolean(compute="_compute_hide_button", default=True)
    hide_approve_bod = fields.Boolean(compute="_compute_hide_button", default=True)

    def _compute_hide_button(self):
        if self.amount_total == 0.0:
            self.hide_confirm_order = self.hide_approve_manager = self.hide_approve_finance = self.hide_approve_bod = True
        elif self.amount_total < 1000000:
            self.hide_approve_manager = self.hide_approve_finance = self.hide_approve_bod = True
            self.hide_confirm_order = False
        elif self.amount_total > 1000000 and self.amount_total < 10000000:
            self.hide_confirm_order = self.hide_approve_finance = self.hide_approve_bod = True
            self.hide_approve_manager = False
        elif self.amount_total > 10000000:
            self.hide_approve_finance = self.hide_approve_bod = False
            self.hide_confirm_order = self.hide_approve_manager = True

    def to_approve_manager(self):
        self.state = 'to_approve_manager'

    def to_approve_finance(self):
        self.state = 'to_approve_finance'

    def to_approve_bod(self):
        self.state = 'to_approve_bod'

    def cancel_po_wizard(self):
        return {
            'name': 'Cancel PO',
            'type': 'ir.actions.act_window',
            'res_model': 'cancel.po.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_purchase_order_id': self.id,
            }
        }

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    price_latest = fields.Float(string='Latest Price', compute='_compute_latest_price')

    @api.depends('product_id')
    def _compute_latest_price(self):
        for line in self:
            get_data = line.env['purchase.order.line'].search(
                [('product_id', '=', line.product_id.id), ('state', 'in', ['done', 'purchase'])],
                order='write_date desc', limit=1)
            line.price_latest = get_data.price_unit