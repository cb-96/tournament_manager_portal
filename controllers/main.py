from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError

class TournamentPortal(http.Controller):

    @http.route(['/my/teams'], auth='user', type='http', website=True)
    def my_teams(self):
        teams = request.env['tournament.team'].sudo().search([('manager_user_id', '=', request.env.user.id)])
        return request.render('tournament_manager_portal.portal_my_teams', {'teams': teams})

    @http.route(['/my/team/<int:team_id>'], auth='user', type='http', website=True)
    def team_view(self, team_id):
        team = request.env['tournament.team'].sudo().browse(team_id)
        if team.manager_user_id.id != request.env.user.id:
            return request.render('website.403')
        memberships = request.env['tournament.membership'].sudo().search([('team_id', '=', team_id)])
        tournament = team.tournament_ids[:1]
        matches = request.env['tournament.match'].sudo().search([
            '|', ('team1_id', '=', team.id), ('team2_id', '=', team.id)
        ], order='date asc')
        return request.render('tournament_manager_portal.portal_team_view', {
            'team': team,
            'roster': [m.player_id for m in memberships],
            'tournament': tournament,
            'matches': matches,
        })

    @http.route(['/my/team/<int:team_id>/add_player'], auth='user', type='http', website=True, methods=['GET','POST'])
    def add_player(self, team_id, **post):
        team = request.env['tournament.team'].sudo().browse(team_id)
        if team.manager_user_id.id != request.env.user.id:
            return request.render('website.403')
        tournament = team.tournament_ids[:1]
        if request.httprequest.method == 'POST':
            player = request.env['tournament.player'].sudo().create({
                'name': post.get('name'),
                'birthdate': post.get('birthdate'),
            })
            request.env['tournament.membership'].sudo().create({
                'team_id': team.id,
                'tournament_id': tournament.id,
                'player_id': player.id,
            })
            return request.redirect('/my/team/%d' % team.id)
        return request.render('tournament_manager_portal.portal_add_player', {
            'team': team,
            'tournament': tournament,
        })

    @http.route(['/my/team/add'], type='http', auth="user", website=True)
    def portal_add_team(self, **kw):
        categories = request.env['team.category'].search([])
        club = request.env.user.partner_id.club_id
        return request.render("tournament_manager_portal.portal_add_team", {
            'categories': categories,
            'club': club,
        })

    @http.route(['/my/team/add'], type='http', auth="user", website=True, methods=['POST'])
    def portal_add_teams_post(self, **post):
        club = request.env.user.partner_id.club_id
        request.env['team.team'].sudo().create({
            'name': post.get('name'),
            'category_id': int(post.get('category_id')),
            'club_id': club.id,
        })
        return request.redirect('/my/teams')

    @http.route(['/my/match/<int:match_id>/pick_lineup'], auth='user', type='http', website=True, methods=['GET', 'POST'])
    def pick_lineup(self, match_id, **post):
        match = request.env['tournament.match'].sudo().browse(match_id)
        user = request.env.user
        # check if user manages one of teams in match
        team = False
        if match.team1_id.manager_user_id.id == user.id:
            team = match.team1_id
        elif match.team2_id.manager_user_id.id == user.id:
            team = match.team2_id
        else:
            return request.render('website.403')
        tournament = match.tournament_id

        roster_memberships = request.env['tournament.membership'].sudo().search([
            ('team_id','=',team.id), ('tournament_id','=',tournament.id)
        ])
        roster_players = [m.player_id for m in roster_memberships]

        selected_player_ids = []
        if request.httprequest.method == 'POST':
            selected_player_ids = [int(pid) for pid in post.getlist('player_ids')]
            # Remove previous lineup:
            request.env['tournament.lineup'].sudo().search([
                ('match_id','=',match.id), ('team_id','=',team.id)
            ]).unlink()
            errors = []
            for player_id in selected_player_ids:
                try:
                    request.env['tournament.lineup'].sudo().create({
                        'match_id': match.id,
                        'team_id': team.id,
                        'player_id': player_id,
                    })
                except ValidationError as e:
                    errors.append(str(e))
            if not errors:
                return request.redirect('/my/team/%d' % team.id)
            else:
                return request.render('tournament_manager_portal.portal_pick_lineup', {
                    'match': match,
                    'team': team,
                    'roster': roster_players,
                    'selected': selected_player_ids,
                    'error': '<br/>'.join(errors)
                })
        else:
            existing_lineup = request.env['tournament.lineup'].sudo().search([
                ('match_id','=',match.id), ('team_id','=',team.id)
            ])
            selected_player_ids = [l.player_id.id for l in existing_lineup]
        return request.render('tournament_manager_portal.portal_pick_lineup', {
            'match': match,
            'team': team,
            'roster': roster_players,
            'selected': selected_player_ids,
        })
