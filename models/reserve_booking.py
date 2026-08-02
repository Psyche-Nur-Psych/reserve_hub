# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime


class ReserveBooking(models.Model):
    _name = 'reserve.booking'
    _description = 'Resource Booking Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'start_datetime desc, id desc'

    name = fields.Char(
        string='Booking Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New')
    )
    title = fields.Char(string='Title / Purpose', required=True, tracking=True)
    user_id = fields.Many2one(
        'res.users',
        string='Requested By',
        default=lambda self: self.env.user,
        required=True,
        tracking=True
    )
    resource_id = fields.Many2one(
        'reserve.resource',
        string='Resource',
        required=True,
        domain="[('state', '=', 'available')]",
        tracking=True
    )
    category_id = fields.Many2one(
        'resource.category',
        related='resource_id.category_id',
        string='Category',
        store=True,
        readonly=True
    )
    start_datetime = fields.Datetime(
        string='Start Time',
        required=True,
        default=fields.Datetime.now,
        tracking=True
    )
    end_datetime = fields.Datetime(
        string='End Time',
        required=True,
        tracking=True
    )
    duration = fields.Float(
        string='Duration (Hours)',
        compute='_compute_duration',
        store=True,
        help='Duration of the booking in hours'
    )
    description = fields.Text(string='Booking Notes / Details')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
        ('done', 'Completed'),
    ], string='Status', default='draft', required=True, tracking=True, copy=False)

    rejection_reason = fields.Text(string='Rejection Reason', tracking=True, copy=False)
    approved_by_id = fields.Many2one(
        'res.users',
        string='Approved/Rejected By',
        readonly=True,
        copy=False,
        tracking=True
    )
    approval_date = fields.Datetime(
        string='Action Date',
        readonly=True,
        copy=False
    )

    @api.depends('start_datetime', 'end_datetime')
    def _compute_duration(self):
        for record in self:
            if record.start_datetime and record.end_datetime:
                delta = record.end_datetime - record.start_datetime
                record.duration = round(delta.total_seconds() / 3600.0, 2)
            else:
                record.duration = 0.0

    @api.constrains('start_datetime', 'end_datetime')
    def _check_valid_dates(self):
        for record in self:
            if record.start_datetime and record.end_datetime:
                if record.end_datetime <= record.start_datetime:
                    raise ValidationError(_('Booking End Time must be later than the Start Time.'))

    @api.constrains('resource_id', 'start_datetime', 'end_datetime', 'state')
    def _check_overlapping_bookings(self):
        """
        Business Rule 1: A resource cannot be booked if another approved or submitted booking
        overlaps the selected time window.
        """
        for record in self:
            if not record.resource_id or not record.start_datetime or not record.end_datetime:
                continue
            if record.state not in ('submitted', 'approved'):
                continue

            # Query for conflicting bookings on the same resource
            overlapping_domain = [
                ('id', '!=', record.id),
                ('resource_id', '=', record.resource_id.id),
                ('state', 'in', ['submitted', 'approved']),
                ('start_datetime', '<', record.end_datetime),
                ('end_datetime', '>', record.start_datetime),
            ]
            overlapping_count = self.search_count(overlapping_domain)
            if overlapping_count > 0:
                overlapping_booking = self.search(overlapping_domain, limit=1)
                raise ValidationError(_(
                    "Conflict Error! Resource '%(resource)s' is already booked/requested from "
                    "%(start)s to %(end)s by %(user)s (Booking Ref: %(ref)s).",
                    resource=record.resource_id.name,
                    start=overlapping_booking.start_datetime,
                    end=overlapping_booking.end_datetime,
                    user=overlapping_booking.user_id.name,
                    ref=overlapping_booking.name or overlapping_booking.title
                ))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('reserve.booking') or _('New')
        return super(ReserveBooking, self).create(vals_list)

    # --- Workflow Actions ---

    def action_submit(self):
        for record in self:
            if record.state != 'draft':
                raise UserError(_('Only draft bookings can be submitted.'))
            record.state = 'submitted'
        return True

    def action_approve(self):
        """Only Managers or Admins can approve bookings"""
        self._check_manager_access()
        for record in self:
            if record.state != 'submitted':
                raise UserError(_('Only pending (submitted) bookings can be approved.'))
            record.write({
                'state': 'approved',
                'approved_by_id': self.env.user.id,
                'approval_date': fields.Datetime.now(),
            })
        return True

    def action_reject(self):
        """Only Managers or Admins can reject bookings"""
        self._check_manager_access()
        for record in self:
            if record.state != 'submitted':
                raise UserError(_('Only pending (submitted) bookings can be rejected.'))
            record.write({
                'state': 'rejected',
                'approved_by_id': self.env.user.id,
                'approval_date': fields.Datetime.now(),
            })
        return True

    def action_cancel(self):
        for record in self:
            if record.state in ('done'):
                raise UserError(_('Completed bookings cannot be cancelled.'))
            record.state = 'cancelled'
        return True

    def action_set_to_draft(self):
        for record in self:
            if record.state not in ('cancelled', 'rejected'):
                raise UserError(_('Only cancelled or rejected bookings can be reset to draft.'))
            record.state = 'draft'
        return True

    def action_mark_done(self):
        for record in self:
            if record.state != 'approved':
                raise UserError(_('Only approved bookings can be marked as completed.'))
            record.state = 'done'
        return True

    def _check_manager_access(self):
        if not (self.env.user.has_group('reserve_hub.group_reserve_hub_manager') or 
                self.env.user.has_group('reserve_hub.group_reserve_hub_admin')):
            raise UserError(_('Permission Denied: Only ReserveHub Managers or Administrators can perform this action.'))
