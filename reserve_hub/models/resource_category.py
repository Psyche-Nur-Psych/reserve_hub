# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResourceCategory(models.Model):
    _name = 'resource.category'
    _description = 'Resource Category'
    _order = 'name'

    name = fields.Char(string='Category Name', required=True, translate=True)
    description = fields.Text(string='Description')
    color = fields.Integer(string='Color Index', default=0)
    active = fields.Boolean(string='Active', default=True)
    
    resource_ids = fields.One2many(
        'reserve.resource',
        'category_id',
        string='Resources'
    )
    resource_count = fields.Integer(
        string='Resource Count',
        compute='_compute_resource_count',
        store=True
    )

    @api.depends('resource_ids')
    def _compute_resource_count(self):
        for category in self:
            category.resource_count = len(category.resource_ids)

    def action_view_resources(self):
        self.ensure_one()
        return {
            'name': 'Resources',
            'type': 'ir.actions.act_window',
            'res_model': 'reserve.resource',
            'view_mode': 'tree,form,kanban',
            'domain': [('category_id', '=', self.id)],
            'context': {'default_category_id': self.id},
        }
