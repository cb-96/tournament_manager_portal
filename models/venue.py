from odoo import models, fields

class TournamentVenue(models.Model):
    _name = 'tournament.venue'
    _description = 'Venue'

    name = fields.Char(string='Venue Name', required=True)
    address = fields.Char(string='Address')
    city = fields.Char(string='City')
    host_club_id = fields.Many2one('tournament.club', string='Host Club', required=True)
    number_of_fields = fields.Integer(string='Number of Fields', default=3)
    description = fields.Text(string='Description')