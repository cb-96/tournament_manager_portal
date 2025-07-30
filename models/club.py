from odoo import models, fields, api

class TournamentClub(models.Model):
    """Represents a sports club."""
    _name = 'tournament.club'
    _description = 'Club'

    club_id = fields.Many2one(
        'res.partner', 
        string='Club', 
        required=True, 
        domain=[('is_company', '=', True)],
        ondelete='cascade',
        help="Reference to the club's partner record"
    )
    manager_ids = fields.Many2many('res.partner', string='Managers', help="Club managers")
    player_ids = fields.Many2many('tournament.player', string='Players', help="Players in the club")
    standing_ids = fields.One2many('tournament.club.standing', 'club_id', string='Standings', help="Club standings per tournament/year")
    name = fields.Char(related='club_id.name', compute='_compute_club_name', store=True, help="Club name")

    @api.depends('club_id')
    def _compute_club_name(self):
        """Compute the club name from the related partner record."""
        for record in self:
            record.name = record.club_id.name if record.club_id else ''