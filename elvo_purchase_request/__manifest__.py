{
    'name': 'elvo_purchase_request',
    'version': '1.0',
    'depends': ['purchase_requisition', 'purchase'],
    'description': """
        Elvo Purchase Request
    """,
    'category': 'invoicing',
    'data': [
        'views/purchase_request.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
