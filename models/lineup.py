from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TournamentLineup(models.Model):
    """Represents a lineup entry for a match (player assigned to a team in a match)."""
    _name = 'tournament.lineup'
    _description = 'Lineup'
    
    match_id = fields.Many2one('tournament.match', required=True, help="Match")
    player_id = fields.Many2one('tournament.player', required=True, help="Player")
    team_id = fields.Many2one('tournament.team', required=True, help="Team")

    @api.model
    def create(self, vals):
        """Ensure player is eligible for the team in the tournament."""
        # --- ELIGIBILITY LOGIC (simplified) ---
        player = self.env['tournament.player'].browse(vals.get('player_id'))
        team = self.env['tournament.team'].browse(vals.get('team_id'))
        match = self.env['tournament.match'].browse(vals.get('match_id'))
        tournament = match.tournament_id
        # Check membership
        membership = self.env['tournament.membership'].search([
            ('player_id', '=', player.id),
            ('team_id', '=', team.id),
            ('tournament_id', '=', tournament.id)
        ], limit=1)
        if not membership:
            raise ValidationError("Player is not registered for this team in this tournament.")
        return super().create(vals)