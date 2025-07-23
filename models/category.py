from odoo import models, fields

class TournamentCategory(models.Model):
    _name = 'tournament.category'
    _description = 'Category'

    name = fields.Char(required=True)