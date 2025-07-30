from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TournamentLineup(models.Model):
    """Represents a lineup entry for a match (players assigned to a team in a match)."""
    _name = 'tournament.lineup'
    _description = 'Lineup'
    
    match_id = fields.Many2one('tournament.match', required=True, help="Match")
    player_id = fields.Many2many('tournament.player', required=True, help="Players in the lineup")
    team_id = fields.Many2one('tournament.team', required=True, help="Team")

    @api.model
    def create(self, vals):
        """Ensure all players are eligible for the team in the tournament."""
        match = self.env['tournament.match'].browse(vals.get('match_id'))
        team = self.env['tournament.team'].browse(vals.get('team_id'))
        player_ids = vals.get('player_id')[0][2] if vals.get('player_id') else []
        tournament = match.tournament_id
        for player_id in player_ids:
            membership = self.env['tournament.membership'].search([
                ('player_id', '=', player_id),
                ('team_id', '=', team.id),
                ('tournament_id', '=', tournament.id)
            ], limit=1)
            if not membership:
                raise ValidationError("One or more players are not registered for this team in this tournament.")
        return super().create(vals)