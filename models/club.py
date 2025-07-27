from odoo import models, fields

#class ResPartner(models.Model):
#    _inherit = 'res.partner'
#
#    is_club_manager = fields.Boolean(string='Is Club Manager', default=False)

class TournamentClub(models.Model):
    #_inherit = 'res.partner'
    _name = 'tournament.club'
    _description = 'Club'

    club_id = fields.Many2one('res.partner', 
                              string='Club', 
                              required=True, 
                              domain=[('is_company', '=', True)],
                              ondelete='cascade')
    manager_ids = fields.Many2many('res.partner', string='Managers')
    player_ids = fields.Many2many('tournament.player', string='Players')