from odoo import models, fields, api

class Tournament(models.Model):
    """Represents a tournament event."""
    _name = 'tournament.tournament'
    _description = "Tournament"

    name = fields.Char(required=True, help="Tournament name")
    tournament_type = fields.Selection([
        ('knockout', 'Knockout'),
        ('round_robin', 'Round Robin'),
        ('groups', 'Groups')
    ], required=True, default='knockout', help="Type of tournament format")
    date_start = fields.Date(help="Start date")
    date_end = fields.Date(help="End date")
    category_ids = fields.Many2many('tournament.category', string='Category', help="Categories included")
    team_ids = fields.Many2many('tournament.team', string='Teams', help="Participating teams")
    match_ids = fields.One2many('tournament.match', 'tournament_id', string='Matches', help="Matches in this tournament")
    season = fields.Char(string='Year', required=False, help="Season or year")

    number_of_teams = fields.Integer(string='Number of Teams', compute='_compute_number_of_teams', store=False, help="Total number of teams in this tournament")

    @api.depends('team_ids')
    def _compute_number_of_teams(self):
        """Compute the number of teams in the tournament."""
        for rec in self:
            rec.number_of_teams = len(rec.team_ids)

class TournamentMatch(models.Model):
    """Represents a match between two teams in a tournament."""
    _name = 'tournament.match'
    _description = "Match"

    tournament_id = fields.Many2one('tournament.tournament', required=True, help="Tournament")
    category_id = fields.Many2one('tournament.category', string='Category', required=True, help="Category")
    team1_id = fields.Many2one('tournament.team', string='Team 1', required=True, help="First team")
    team2_id = fields.Many2one('tournament.team', string='Team 2', required=True, help="Second team")
    date = fields.Datetime(help="Match date and time")
    score_team1 = fields.Integer(string='Score Team 1', help="Score for team 1")
    score_team2 = fields.Integer(string='Score Team 2', help="Score for team 2")
    state = fields.Selection([
        ('scheduled', 'Scheduled'),
        ('done', 'Done')
    ], default='scheduled', help="Match state")

    def get_result_display(self):
        """Return a string representation of the match result."""
        self.ensure_one()
        if self.state == 'done':
            return f"{self.team1_id.name} {self.score_team1} - {self.score_team2} {self.team2_id.name}"
        return "Match not played yet"

class TournamentClubStanding(models.Model):
    """Represents a club's standing in a tournament."""
    _name = 'tournament.club.standing'
    _description = "Club Standing"

    club_id = fields.Many2one('tournament.club', string='Club', required=True, help="Club")
    tournament_id = fields.Many2one('tournament.tournament', string='Tournament', required=True, help="Tournament")
    points = fields.Integer(string='Points', default=0, help="Total points")
    matches_played = fields.Integer(string='Matches Played', default=0, help="Number of matches played")
    wins = fields.Integer(string='Wins', default=0, help="Number of wins")
    draws = fields.Integer(string='Draws', default=0, help="Number of draws")
    losses = fields.Integer(string='Losses', default=0, help="Number of losses")
    goals_for = fields.Integer(string='Points For', default=0, help="Goals scored")
    goals_against = fields.Integer(string='Points Against', default=0, help="Goals conceded")

    goal_difference = fields.Integer(string='Goal Difference', compute='_compute_goal_difference', store=False, help="Goals for minus goals against")

    @api.depends('goals_for', 'goals_against')
    def _compute_goal_difference(self):
        """Compute the goal difference for the club standing."""
        for rec in self:
            rec.goal_difference = rec.goals_for - rec.goals_against