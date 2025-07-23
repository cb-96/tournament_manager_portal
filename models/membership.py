from odoo import models, fields

class TournamentMembership(models.Model):
    _name = 'tournament.membership'
    _description = 'Team Membership'

    tournament_id = fields.Many2one('tournament.tournament', required=True)
    player_id = fields.Many2one('tournament.player', required=True)
    team_id = fields.Many2one('tournament.team', required=True)
    is_current = fields.Boolean(default=True)