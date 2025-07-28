from odoo import models, fields

class TournamentClub(models.Model):
    _name = 'tournament.club'
    _description = 'Club'

    club_id = fields.Many2one('res.partner', 
                              string='Club', 
                              required=True, 
                              domain=[('is_company', '=', True)],
                              ondelete='cascade')
    manager_ids = fields.Many2many('res.partner', string='Managers')
    player_ids = fields.Many2many('tournament.player', string='Players')
    name = fields.Char(related='club_id.name', compute='_compute_club_name', store=True)

    @api.depends('club_id')
    def _compute_club_name(self):
        for record in self:
            record.name = record.club_id.name if record.club_id else ''