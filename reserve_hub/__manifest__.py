{
    'name': 'ReserveHub - Smart Resource Booking System',
    'version': '19.0.1.0.0',
    'category': 'Services/Resource Management',
    'summary': 'Smart resource booking, room reservation, equipment scheduling, and utilization analytics.',
    'description': """
ReserveHub - Smart Resource Booking System for Odoo 19
======================================================
ReserveHub is an enterprise-grade resource booking application designed for modern organizations.
Effortlessly schedule conference rooms, vehicles, projectors, laptops, and IT hardware.

Key Features:
-------------
* **Resource Directory**: Rich Kanban cards with live availability badges and HSL color coding.
* **Smart Booking Workflow**: Auto-computed duration with collision/overlap validation.
* **Interactive Calendar**: Resource reservation calendar view with quick previews.
* **Utilization Analytics**: Built-in Pivot matrix and Bar/Pie utilization charts.
* **Security & Roles**: Multi-tier access security (Employees vs Managers).
    """,
    'author': 'Antigravity / ReserveHub Team',
    'website': 'https://github.com/Psyche-Nur-Psych/reserve_hub',
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'web'],
    'data': [
        'security/reserve_hub_groups.xml',
        'security/ir.model.access.csv',
        'security/reserve_hub_security.xml',
        'views/res_config_settings_views.xml',
        'views/resource_category_views.xml',
        'views/reserve_resource_views.xml',
        'views/reserve_booking_views.xml',
        'views/dashboard_views.xml',
        'views/menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'reserve_hub/static/src/css/reserve_hub_style.css',
        ],
    },
    'images': ['static/description/banner_kanban.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
