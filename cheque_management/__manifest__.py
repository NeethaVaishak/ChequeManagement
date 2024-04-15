{
    'name': "Cheque Management",
    'version': '15.0',
    'author': "Neetha",
    'category': 'Category',
    'description': """This module allows you to manage cheque""",
    'depends': ['base','account'],
    'data': [
        'security/cheque_security.xml',
        'security/ir.model.access.csv',
        'data/cheque_management_data.xml',
        'views/payment_receipt_report_inherited.xml',
        'views/cheque_management_view.xml',
        'views/payment_signature.xml',


    ],
}

