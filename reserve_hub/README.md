# ReserveHub – Smart Resource Booking System (Odoo 19)

**ReserveHub** is an Odoo 19 enterprise module designed for managing shared organizational resources—such as conference rooms, vehicles, IT/AV equipment, and workstations—with a manager approval workflow, conflict prevention, interactive calendar views, access control, and analytics dashboards.

---

## Key Features

- 🏢 **Resource & Category Management**: Categorize shared assets with custom tags, specs, capacity, location, images, and status tracking (`Available`, `Under Maintenance`, `Out of Service`).
- 📅 **Interactive Calendar & Booking Workflow**: Create booking requests with automatic calculation of duration in hours.
- ⚡ **Overlap Prevention & Conflict Checking**: Built-in validation rule (`@api.constrains`) preventing overlapping bookings for the same resource during approved or pending states.
- 🛡️ **Multi-Tier Security & Approval Matrix**:
  - **Employee**: Browse resources, view availability, and submit booking requests.
  - **Manager**: Review pending requests, approve/reject bookings, manage resources and categories.
  - **Administrator**: Complete module control, security configuration, and administrative overrides.
- 📊 **Analytics & Utilization Dashboards**: Pivot and graph views analyzing total booked hours, request status breakdown, and resource utilization.
- 🔒 **Read-Only Completion State**: Completed, approved, or rejected bookings are locked to preserve audit trail integrity.

---

## Technical Specifications

| Parameter | Value |
| --- | --- |
| **Odoo Version** | Odoo 19.0 |
| **Python Version** | Python 3.10+ |
| **License** | LGPL-3 |
| **Dependencies** | `base`, `mail`, `web` |
| **Models** | `resource.category`, `reserve.resource`, `reserve.booking` |

---

## Installation & Deployment Guide

### Prerequisites
- Odoo 19 server running with PostgreSQL.
- Access to custom addons directory.

### Step-by-Step Setup
1. **Copy Module**: Copy or clone the `reserve_hub` directory into your Odoo custom addons directory (`/path/to/odoo/custom_addons/reserve_hub`).
2. **Restart Odoo**: Restart your Odoo server instance to register the new module.
   ```bash
   ./odoo-bin -c /etc/odoo.conf -u reserve_hub --stop-after-init
   ```
3. **Update App List**:
   - Log into Odoo as an Administrator.
   - Activate **Developer Mode** under Settings.
   - Navigate to **Apps** > **Update Apps List**.
4. **Install ReserveHub**:
   - Search for `ReserveHub` in the Apps list.
   - Click **Install**.

---

## User Roles & Security Configuration

Assign user roles via **Settings** > **Users & Companies** > **Users** under the **ReserveHub** security section:

| Role | Security Group ID | Capabilities |
| --- | --- | --- |
| **Employee** | `group_reserve_hub_employee` | Read resources & calendar, create draft bookings, submit requests, cancel own draft bookings. |
| **Manager** | `group_reserve_hub_manager` | All Employee permissions + approve/reject booking requests, create/edit resources and categories, access analytics. |
| **Administrator** | `group_reserve_hub_admin` | All Manager permissions + security config, module settings, data administration. |

---

## Workflow Guide

```
+--------+       action_submit()       +-----------+
| Draft  |  ------------------------>  | Submitted |  (Pending Manager Review)
+--------+                             +-----------+
    |                                    /       \
    | action_cancel()   action_approve()/         \ action_reject()
    v                                  v           v
+-----------+                    +----------+   +----------+
| Cancelled |                    | Approved |   | Rejected |
+-----------+                    +----------+   +----------+
                                       |
                                       | action_mark_done()
                                       v
                                 +-----------+
                                 | Completed |  (Read-Only Audit Record)
                                 +-----------+
```

1. **Submit Request**: Employee creates a booking, fills in title, resource, and start/end time, then clicks **Submit Request**.
2. **Conflict Check**: System verifies whether any existing `submitted` or `approved` booking overlaps with the chosen timeframe for that resource.
3. **Manager Review**: Managers receive pending requests under the **Pending Approval** menu option and review details.
4. **Approval / Rejection**:
   - Click **Approve**: Status changes to `Approved`, recording approver ID and timestamp.
   - Click **Reject**: Status changes to `Rejected`.
5. **Completion**: Once the event finishes, click **Mark Completed** to lock the record.

---

## Project Structure

```
reserve_hub/
├── __manifest__.py                 # Module manifest metadata
├── __init__.py                     # Package initialization
├── models/
│   ├── __init__.py                 # Model registration
│   ├── resource_category.py        # Category model definition
│   ├── reserve_resource.py         # Resource model definition
│   └── reserve_booking.py          # Booking request model & workflow logic
├── security/
│   ├── reserve_hub_groups.xml      # Security groups (Employee, Manager, Admin)
│   ├── ir.model.access.csv         # Access rights table (ACL)
│   └── reserve_hub_security.xml    # Record rules
├── views/
│   ├── menu_views.xml              # Navigation hierarchy and menu items
│   ├── resource_category_views.xml # Category tree, form, search views
│   ├── reserve_resource_views.xml  # Resource kanban, list, form views
│   ├── reserve_booking_views.xml   # Booking form, list, calendar views
│   └── dashboard_views.xml         # Analytics pivot and graph views
├── data/
│   └── reserve_hub_demo.xml        # Sample demo categories, resources & bookings
├── README.md                       # User & Administrator guide
└── DOCS.md                         # Technical architecture reference
```

---

## License

Licensed under the **GNU Lesser General Public License v3.0 (LGPL-3)**.
