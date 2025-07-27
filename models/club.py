from odoo import models, fields

#class ResPartner(models.Model):
#    _inherit = 'res.partner'
#
#    is_club_manager = fields.Boolean(string='Is Club Manager', default=False)

class TournamentClub(models.Model):
    #_inherit = 'res.partner'
    _name = 'tournament.club'
    _description = 'Club'

    name = fields.Char(required=True)
    manager_ids = fields.Many2many('res.users', string='Managers')
    player_ids = fields.Many2many('tournament.player', string='Players')