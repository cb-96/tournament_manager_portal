from odoo import models, fields

class TournamentClub(models.Model):
    _name = 'tournament.club'
    _description = 'Club'

    name = fields.Char(required=True)