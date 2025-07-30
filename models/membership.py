from odoo import models, fields

class TournamentMembership(models.Model):
    """Links a player to a team for a specific tournament."""
    _name = 'tournament.membership'
    _description = 'Team Membership'

    tournament_id = fields.Many2one('tournament.tournament', required=True, help="Tournament")
    player_id = fields.Many2one('tournament.player', required=True, help="Player")
    team_id = fields.Many2one('tournament.team', required=True, help="Team")
    is_current = fields.Boolean(default=True, help="Is current membership?")