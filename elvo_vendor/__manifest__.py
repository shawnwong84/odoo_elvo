{
    'name': 'elvo_vendor',
    'version': '1.0',
    'depends': ['base', 'l10n_it_edi'],
    'description': """
        Elvo Vendor
    """,
    'category': 'invoicing',
    'data': [
        'views/elvo_vendor.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
