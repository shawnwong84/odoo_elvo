{
    'name': 'elvo_account',
    'version': '1.0',
    'depends': ['account', 'elvo_purchase_order'],
    'description': """
        Elvo Account
    """,
    'category': 'invoicing',
    'data': [
        'views/elvo_account.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
