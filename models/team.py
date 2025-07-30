from odoo import api, models, fields
from odoo.exceptions import ValidationError

class TournamentTeam(models.Model):
    """Represents a team participating in tournaments."""
    _name = 'tournament.team'
    _description = "Team"

    name = fields.Char(required=True, help="Team name")
    club_id = fields.Many2one('tournament.club', string='Club', required=True, help="Associated club")
    category_id = fields.Many2one('tournament.category', string='Category', required=True, help="Team category")
    level = fields.Integer(string='Team Level', default=1, help="1=A, 2=B, 3=C, etc.")
    manager_user_id = fields.Many2one('res.partner', string="Manager", help="Team manager")
    membership_ids = fields.One2many('tournament.membership', 'team_id', string="Memberships", help="Memberships for this team")
    tournament_ids = fields.Many2many('tournament.tournament', string="Tournaments", help="Tournaments this team participates in")

    @api.model
    def create(self, vals):
        """Ensure only club managers can create teams for their clubs."""
        club_id = vals.get('club_id')
        if not club_id:
            raise ValidationError("Club must be specified.")
        club = self.env['tournament.club'].browse(club_id)
        if not club.exists():
            raise ValidationError("Selected club does not exist.")
        if self.env.user.partner_id not in club.manager_ids:
            raise ValidationError("You can only create teams for clubs you manage.")
        return super().create(vals)
