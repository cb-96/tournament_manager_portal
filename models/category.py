from odoo import models, fields


class TournamentCategory(models.Model):
    """Represents a category for tournaments (e.g., age group, skill level)."""
    _name = 'tournament.category'
    _description = 'Category'

    name = fields.Char(required=True, help="Category name")