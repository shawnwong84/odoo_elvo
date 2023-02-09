{
    'name': 'elvo_inventory',
    'version': '1.0',
    'depends': ['stock', 'elvo_customer_retur'],
    'description': """
        Elvo Inventory
    """,
    'category': 'inventory',
    'data': [
        'views/elvo_inventory.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
