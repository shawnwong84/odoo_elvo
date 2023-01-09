{
    'name': 'elvo_purchase_order',
    'version': '1.0',
    'depends': ['purchase'],
    'description': """
        Elvo Purchase Order
    """,
    'category': 'invoicing',
    'data': [
        'views/purchase_order.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
