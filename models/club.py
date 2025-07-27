from odoo import models, fields

class TournamentClub(models.Model):
    #_inherit = 'res.partner'
    _name = 'tournament.club'
    _description = 'Club'

    name = fields.Char(required=True)
    manager_ids = fields.Many2many('res.users', string='Managers')
    player_ids = fields.Many2many('tournament.player', string='Players')