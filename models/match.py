from odoo import models, fields, api
from datetime import datetime, timedelta, time

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
    days_count = fields.Integer(string='Number of Days', required=True, default=1, help="How many days the tournament lasts")
    day_start_time = fields.Float(string='Day Start Time', required=True, default=9.0, help="Start time each day (e.g. 9.0 for 9:00)")
    day_end_time = fields.Float(string='Day End Time', required=True, default=18.0, help="End time each day (e.g. 18.0 for 18:00)")
    category_ids = fields.Many2many('tournament.category', string='Category', help="Categories included")
    team_ids = fields.Many2many('tournament.team', string='Teams', help="Participating teams")
    match_ids = fields.One2many('tournament.match', 'tournament_id', string='Matches', help="Matches in this tournament")
    season = fields.Char(string='Year', required=False, help="Season or year")
    match_duration_minutes = fields.Integer(
        string='Match Duration (minutes)', required=True, default=60,
        help="Duration of each match in minutes. Used to calculate number of matches per day.")

    number_of_teams = fields.Integer(string='Number of Teams', compute='_compute_number_of_teams', store=False, help="Total number of teams in this tournament")

    @api.depends('team_ids')
    def _compute_number_of_teams(self):
        """Compute the number of teams in the tournament."""
        for rec in self:
            rec.number_of_teams = len(rec.team_ids)

    def generate_schedule(self):
        """Generate the match schedule based on tournament type."""
        if self.tournament_type == 'knockout':
            self._generate_knockout_schedule()
        elif self.tournament_type == 'round_robin':
            self._generate_round_robin_schedule()
        # Add more types as needed

    def _generate_knockout_schedule(self):
        """Generate a bracket (knockout) schedule."""
        teams = list(self.team_ids)
        if len(teams) < 2:
            return
        matches = []
        round_teams = teams
        round_num = 1
        while len(round_teams) > 1:
            next_round = []
            for i in range(0, len(round_teams), 2):
                if i+1 < len(round_teams):
                    matches.append((round_teams[i], round_teams[i+1], round_num))
                    next_round.append(None)  # Placeholder for winner
            round_teams = next_round
            round_num += 1
        self._assign_match_times(matches)

    def _generate_round_robin_schedule(self):
        """Generate a round robin schedule (all vs all)."""
        teams = list(self.team_ids)
        matches = []
        for i in range(len(teams)):
            for j in range(i+1, len(teams)):
                matches.append((teams[i], teams[j], 1))  # round=1 for all
        self._assign_match_times(matches)

    def _assign_match_times(self, matches):
        """Assigns match times over the tournament days and time slots, using match duration."""
        start_date = self.date_start or fields.Date.today()
        day_count = self.days_count or 1
        start_time = self.day_start_time or 9.0
        end_time = self.day_end_time or 18.0
        match_duration = self.match_duration_minutes or 60
        # Calculate number of matches per day
        total_minutes = int((end_time - start_time) * 60)
        slots_per_day = total_minutes // match_duration
        match_idx = 0
        for day in range(day_count):
            for slot in range(slots_per_day):
                if match_idx >= len(matches):
                    break
                team1, team2, round_num = matches[match_idx]
                match_time = (start_time * 60) + (slot * match_duration)
                hour = int(match_time // 60)
                minute = int(match_time % 60)
                match_datetime = datetime.combine(
                    fields.Date.from_string(start_date) + timedelta(days=day),
                    time(hour, minute)
                )
                self.env['tournament.match'].create({
                    'tournament_id': self.id,
                    'team1_id': team1.id,
                    'team2_id': team2.id,
                    'date': match_datetime,
                })
                match_idx += 1
            if match_idx >= len(matches):
                break

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