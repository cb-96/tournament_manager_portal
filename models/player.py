from odoo import models, fields

class TournamentPlayer(models.Model):
    """Represents a player who can participate in tournaments."""
    _name = 'tournament.player'
    _description = 'Player'

    name = fields.Char(required=True, help="Player's full name")
    birthdate = fields.Date(help="Date of birth")