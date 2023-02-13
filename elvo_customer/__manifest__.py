{
    'name': 'elvo_customer',
    'version': '1.0',
    'depends': ['elvo_marketplace'],
    'description': """
        Elvo Customer
    """,
    'category': 'invoicing',
    'data': [
        'views/master_customer.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
