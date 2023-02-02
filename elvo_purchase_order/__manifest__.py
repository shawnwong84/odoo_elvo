{
    'name': 'elvo_purchase_order',
    'version': '1.0',
    'depends': ['purchase', 'purchase_stock'],
    'description': """
        Elvo Purchase Order
    """,
    'category': 'invoicing',
    'data': [
        'views/purchase_order.xml',
        'views/elvo_product_supplier.xml',
        'views/stock_picking.xml',
        'views/elvo_request_for_quotation.xml',
        'security/ir.model.access.csv',
        'security/access_groups.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
