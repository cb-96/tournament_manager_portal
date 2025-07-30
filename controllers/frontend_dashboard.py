from odoo import http
from odoo.http import request
import json

class TournamentDashboardController(http.Controller):
    @http.route('/tournament/frontend_dashboard', type='http', auth='user', website=True)
    def tournament_frontend_dashboard(self, **kw):
        # Get upcoming matches grouped by date
        matches = request.env['tournament.match'].sudo().search([('date', '>=', fields.Datetime.now())], order='date asc')
        match_days = {}
        for match in matches:
            day = match.date.date().isoformat() if match.date else 'Unknown'
            match_days.setdefault(day, 0)
            match_days[day] += 1
        days = list(match_days.keys())
        counts = list(match_days.values())
        return request.render('tournament_manager_portal.tournament_frontend_dashboard_template', {
            'days': json.dumps(days),
            'counts': json.dumps(counts),
        })

    @http.route('/tournament/bracket/<int:tournament_id>', type='http', auth='user', website=True)
    def tournament_bracket(self, tournament_id, **kw):
        tournament = request.env['tournament.tournament'].sudo().browse(tournament_id)
        # Get all matches for this tournament, grouped by round and category
        matches = request.env['tournament.match'].sudo().search([('tournament_id', '=', tournament_id)], order='date asc')
        bracket_data = {}
        for match in matches:
            cat = match.category_id.name if match.category_id else 'General'
            round_num = getattr(match, 'round_num', 1)  # You may want to add a round_num field
            bracket_data.setdefault(cat, {})
            bracket_data[cat].setdefault(round_num, [])
            bracket_data[cat][round_num].append({
                'team1': match.team1_id.name,
                'team2': match.team2_id.name,
                'score1': match.score_team1,
                'score2': match.score_team2,
                'state': match.state,
            })
        return request.render('tournament_manager_portal.tournament_bracket_template', {
            'tournament': tournament,
            'bracket_data': json.dumps(bracket_data),
        })

    @http.route('/tournament/dashboard', type='http', auth='user', website=True)
    def tournament_dashboard(self, **kw):
        # Fetch club standings for the latest tournament
        tournament = request.env['tournament.tournament'].search([], order='date_start desc', limit=1)
        standings = request.env['tournament.club.standing'].search([
            ('tournament_id', '=', tournament.id)
        ])
        clubs = [s.club_id.name for s in standings]
        points = [s.points for s in standings]
        return request.render('tournament_manager_portal.tournament_dashboard_template', {
            'tournament': tournament,
            'clubs': clubs,
            'points': points,
        })
