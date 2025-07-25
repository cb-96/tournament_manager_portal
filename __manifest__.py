{
    'name': "Tournament Manager Portal",
    'version': "18.0",
    'author': "Cedric Bouckaert",
    'category': "Website",
    'website': "http://192.168.178.68:8069",
    'summary': "Let team managers create players and lineups for matches via Odoo Website Portal.",
    'depends': ['website', 'portal'],
    'data': [
        'security/ir.model.access.csv',
	'views/portal_views.xml',
        'views/templates.xml',
        'views/backend_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
