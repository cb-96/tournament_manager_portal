from odoo import http
from odoo.http import request

class TournamentDashboardController(http.Controller):
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
