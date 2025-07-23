from odoo import models, fields

class TournamentPlayer(models.Model):
    _name = 'tournament.player'
    _description = 'Player'

    name = fields.Char(required=True)
    birthdate = fields.Date()