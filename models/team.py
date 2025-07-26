from odoo import api, models, fields
from odoo.exceptions import ValidationError

class TournamentTeam(models.Model):
    _name = 'tournament.team'
    _description = "Team"

    name = fields.Char(required=True)
    club_id = fields.Many2one('tournament.club', string='Club', required=True)
    category_id = fields.Many2one('tournament.category', string='Category', required=True)
    level = fields.Integer(string='Team Level', default=1)  # 1=A, 2=B, 3=C etc
    manager_user_id = fields.Many2one('res.users', string="Manager")
    # link with memberships:
    membership_ids = fields.One2many('tournament.membership', 'team_id', string="Memberships")
    tournament_ids = fields.Many2many('tournament.tournament', string="Tournaments")

    @api.model
    def create(self, vals):
        club = self.env['tournament.club'].browse(vals.get('club_id'))
        if self.env.user not in club.manager_ids:
            raise ValidationError("You can only create teams for clubs you manage.")
        return super().create(vals)

class TournamentTeamManager(models.Model):
    _name = 'tournament.team.manager'
    _description = "Team Manager"

    name = fields.Char(required=True)
    team_id = fields.Many2one('tournament.team', string='Team', required=True)
    user_id = fields.Many2one('res.users', string='User', required=True)
    role = fields.Selection([
        ('manager', 'Manager'),
        ('assistant', 'Assistant')
    ], default='manager', string='Role')

    @api.constrains('team_id', 'user_id')
    def _check_unique_manager(self):
        for record in self:
            if self.search_count([('team_id', '=', record.team_id.id), ('user_id', '=', record.user_id.id)]) > 1:
                raise ValidationError("This user is already a manager for this team.")