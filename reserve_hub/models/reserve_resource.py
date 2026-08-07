# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ReserveResource(models.Model):
    _name = 'reserve.resource'
    _description = 'Reservable Resource'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'category_id, name'

    name = fields.Char(string='Resource Name', required=True, tracking=True)
    code = fields.Char(string='Resource Code', copy=False, help='Unique identifier for the resource')
    category_id = fields.Many2one(
        'resource.category',
        string='Category',
        required=True,
        ondelete='restrict',
        tracking=True
    )
    description = fields.Text(string='Description/Specs')
    location = fields.Char(string='Location / Room', tracking=True)
    capacity = fields.Integer(string='Capacity / Persons', default=1, tracking=True)
    active = fields.Boolean(string='Active', default=True)
    image_1920 = fields.Image(string='Image', max_width=1920, max_height=1920)
    responsible_id = fields.Many2one(
        'res.users',
        string='Responsible Manager',
        default=lambda self: self.env.user,
        tracking=True
    )
    state = fields.Selection([
        ('available', 'Available'),
        ('maintenance', 'Under Maintenance'),
        ('archived', 'Out of Service'),
    ], string='Status', default='available', tracking=True)

    booking_ids = fields.One2many('reserve.booking', 'resource_id', string='Bookings')
    booking_count = fields.Integer(
        string='Total Bookings',
        compute='_compute_booking_count'
    )

    @api.depends('booking_ids')
    def _compute_booking_count(self):
        for record in self:
            record.booking_count = len(record.booking_ids)

    def action_view_bookings(self):
        self.ensure_one()
        return {
            'name': f'Bookings for {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'reserve.booking',
            'view_mode': 'calendar,tree,form,pivot,graph',
            'domain': [('resource_id', '=', self.id)],
            'context': {'default_resource_id': self.id},
        }
