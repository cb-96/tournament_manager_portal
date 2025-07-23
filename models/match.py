from odoo import models, fields

class Tournament(models.Model):
    _name = 'tournament.tournament'
    _description = "Tournament"

    name = fields.Char(required=True)
    tournament_type = fields.Selection([
        ('knockout', 'Knockout'),
        ('round_robin', 'Round Robin'),
        ('groups', 'Groups')
    ], required=True, default='knockout')
    date_start = fields.Date()
    date_end = fields.Date()
    team_ids = fields.Many2many('tournament.team', string='Teams')
    match_ids = fields.One2many('tournament.match', 'tournament_id', string='Matches')

class TournamentMatch(models.Model):
    _name = 'tournament.match'
    _description = "Match"

    tournament_id = fields.Many2one('tournament.tournament', required=True)
    team1_id = fields.Many2one('tournament.team', string='Team 1', required=True)
    team2_id = fields.Many2one('tournament.team', string='Team 2', required=True)
    date = fields.Datetime()
    score_team1 = fields.Integer(string='Score Team 1')
    score_team2 = fields.Integer(string='Score Team 2')
    state = fields.Selection([
        ('scheduled', 'Scheduled'),
        ('done', 'Done')
    ], default='scheduled')