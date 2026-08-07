# -*- coding: utf-8 -*-
{
    'name': 'ReserveHub - Smart Resource Booking System',
    'version': '19.0.1.0.0',
    'category': 'Services/Resource Management',
    'summary': 'Manage shared resources and handle booking requests with manager approval workflows',
    'description': """
ReserveHub - Smart Resource Booking System for Odoo 19
======================================================

Key Features:
-------------
* **Resource & Category Management**: Organize equipment, meeting rooms, vehicles, and workspaces.
* **Booking Requests**: Seamless creation of booking requests with date and time ranges.
* **Approval Workflow**: Multi-state workflow (Draft -> Submitted -> Approved / Rejected -> Done).
* **Conflict & Overlap Prevention**: Automated check against overlapping bookings for the same resource.
* **Calendar View**: Visual overview of resource reservations over days, weeks, and months.
* **Security & Access Control**: Granular roles for Employee, Manager, and Administrator.
* **Analytics & Dashboard**: Pivot and graph views for tracking resource utilization and status metrics.
    """,
    'author': 'Antigravity / ReserveHub Team',
    'website': 'https://www.example.com/reservehub',
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'web'],
    'data': [
        'security/reserve_hub_groups.xml',
        'security/ir.model.access.csv',
        'security/reserve_hub_security.xml',
        'views/resource_category_views.xml',
        'views/reserve_resource_views.xml',
        'views/reserve_booking_views.xml',
        'views/dashboard_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [
        'data/reserve_hub_demo.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
