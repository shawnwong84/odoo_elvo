# -*- coding: utf-8 -*-
{
    'name' : "Advance Payment for Sale and Purchase",
    'version': '14.0.1.1',
    'summary': 'App Vendor Advance Payment for Sale Purchase Advance Payment Sale Advance Payment Customer Advance Payment Vendor Payment Adjustment Account Advance Payment Vendor Bill Advance Payment Sale Order Advance Payment Purchase Order Advance Payment for Vendor',
    'description' : """
     """,
    "license" : "OPL-1",
    'depends' : ['sale_management','purchase','account','akm_payment_multi_deduction'],
    'data': [
                'security/advance_payment_group.xml',
                'security/ir.model.access.csv',
                'views/res_config_view.xml',
                # 'views/sale_order_view.xml',
                # 'views/purchase_order_view.xml',
                'views/payment_view.xml',
                'wizard/sale_advance_payment_wizard.xml',
                'wizard/purchase_advance_payment_wizard.xml',
             ],
    'installable': True,
    'auto_install': False,
    'price': 10,
    'currency': "EUR",
    'category': 'Accounting',
}
