from odoo import models, fields

class TournamentClub(models.Model):
    _name = 'tournament.club'
    _description = 'Club'

    club_id = fields.Many2one('res.partner', 
                              string='Club', 
                              required=True, 
                              domain=[('is_company', '=', True)],
                              ondelete='cascade')
    related = 'club_id.name'
    manager_ids = fields.Many2many('res.partner', string='Managers')
    player_ids = fields.Many2many('tournament.player', string='Players')