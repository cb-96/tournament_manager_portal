from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TournamentLineup(models.Model):
    _name = 'tournament.lineup'
    _description = 'Lineup'
    
    match_id = fields.Many2one('tournament.match', required=True)
    player_id = fields.Many2one('tournament.player', required=True)
    team_id = fields.Many2one('tournament.team', required=True)

    @api.model
    def create(self, vals):
        # --- ELIGIBILITY LOGIC (simplified) ---
        # You can expand this with your full constraint logic!
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
            # check for B->A or similar - for brevity, not duplicated here.
            raise ValidationError("Player is not registered for this team in this tournament.")
        return super().create(vals)