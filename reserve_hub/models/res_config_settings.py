from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    reserve_hub_auto_approve = fields.Boolean(
        string="Auto-Approve Bookings",
        help="Automatically approve booking requests if resources are available.",
        config_parameter='reserve_hub.auto_approve'
    )
    reserve_hub_max_duration = fields.Integer(
        string="Max Duration (Hours)",
        default=8,
        config_parameter='reserve_hub.max_duration'
    )
    reserve_hub_buffer_time = fields.Integer(
        string="Buffer Time (Minutes)",
        default=15,
        config_parameter='reserve_hub.buffer_time'
    )
    reserve_hub_send_email = fields.Boolean(
        string="Send Email Alerts",
        default=True,
        config_parameter='reserve_hub.send_email'
    )
