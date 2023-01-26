{
    'name': 'elvo_customer_retur',
    'version': '1.0',
    'depends': ['base', 'sale', 'account'],
    'description': """
        Elvo Customer Retur
    """,
    'category': 'invoicing',
    'data': [
        'views/customer_retur.xml',
        'views/account_move_reversal.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
