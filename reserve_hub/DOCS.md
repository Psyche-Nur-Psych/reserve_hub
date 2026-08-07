# ReserveHub Technical Architecture & API Documentation

This document provides in-depth technical documentation for developers, system integrators, and maintainers of the `reserve_hub` Odoo 19 module.

---

## 1. Model Schemas

### 1.1 `resource.category`
- **Description**: Model for organizing resources into logical groups (e.g. Meeting Rooms, Vehicles, IT Equipment).
- **Technical Name**: `resource.category`
- **Inherits**: `base`

| Field Name | Type | Options / Attributes | Description |
| --- | --- | --- | --- |
| `name` | Char | required=True, translate=True | Category display name |
| `description` | Text | - | Detailed description |
| `color` | Integer | default=0 | Odoo tag color index for visual UI coding |
| `active` | Boolean | default=True | Active status flag |
| `resource_ids` | One2many | 'reserve.resource', 'category_id' | Associated resources |
| `resource_count` | Integer | compute='_compute_resource_count', store=True | Total count of resources in category |

---

### 1.2 `reserve.resource`
- **Description**: Represents an individual shared asset that can be booked.
- **Technical Name**: `reserve.resource`
- **Inherits**: `mail.thread`, `mail.activity.mixin`

| Field Name | Type | Options / Attributes | Description |
| --- | --- | --- | --- |
| `name` | Char | required=True, tracking=True | Resource display name |
| `code` | Char | copy=False | Unique code / tag |
| `category_id` | Many2one | 'resource.category', required=True | Category reference |
| `description` | Text | - | Technical specs and notes |
| `location` | Char | tracking=True | Physical location / room number |
| `capacity` | Integer | default=1, tracking=True | Max seating capacity / units |
| `active` | Boolean | default=True | Active flag |
| `image_1920` | Image | max_width=1920, max_height=1920 | Photo thumbnail of the resource |
| `responsible_id`| Many2one | 'res.users', default=current_user | Assigned manager responsible |
| `state` | Selection | ('available', 'maintenance', 'archived') | Operational status |
| `booking_ids` | One2many | 'reserve.booking', 'resource_id' | Booking history |
| `booking_count` | Integer | compute='_compute_booking_count' | Total bookings count |

---

### 1.3 `reserve.booking`
- **Description**: Transactional request model for scheduling resources.
- **Technical Name**: `reserve.booking`
- **Inherits**: `mail.thread`, `mail.activity.mixin`

| Field Name | Type | Options / Attributes | Description |
| --- | --- | --- | --- |
| `name` | Char | required=True, default='New' | Unique booking reference |
| `title` | Char | required=True, tracking=True | Title or purpose of booking |
| `user_id` | Many2one | 'res.users', required=True, default=current_user | Requester |
| `resource_id` | Many2one | 'reserve.resource', required=True | Target resource |
| `category_id` | Many2one | related='resource_id.category_id', store=True | Related category |
| `start_datetime`| Datetime | required=True, tracking=True | Booking start datetime |
| `end_datetime` | Datetime | required=True, tracking=True | Booking end datetime |
| `duration` | Float | compute='_compute_duration', store=True | Calculated duration in hours |
| `description` | Text | - | Agenda or special notes |
| `state` | Selection | ('draft', 'submitted', 'approved', 'rejected', 'cancelled', 'done') | Booking workflow status |
| `rejection_reason`| Text | tracking=True | Manager reason for rejection |
| `approved_by_id` | Many2one| 'res.users', readonly=True | Manager who approved/rejected |
| `approval_date` | Datetime | readonly=True | Timestamp of approval/rejection |

---

## 2. Business Rules & Python Constraints

### 2.1 Overlap Constraint (`_check_overlapping_bookings`)
Implemented using `@api.constrains('resource_id', 'start_datetime', 'end_datetime', 'state')`:
```python
overlapping_domain = [
    ('id', '!=', record.id),
    ('resource_id', '=', record.resource_id.id),
    ('state', 'in', ['submitted', 'approved']),
    ('start_datetime', '<', record.end_datetime),
    ('end_datetime', '>', record.start_datetime),
]
```
If `search_count(overlapping_domain) > 0`, a `ValidationError` is raised.

### 2.2 Datetime Validation Constraint (`_check_valid_dates`)
Implemented using `@api.constrains('start_datetime', 'end_datetime')`:
Ensures `end_datetime > start_datetime`. Otherwise, a `ValidationError` is raised.

### 2.3 Manager Permission Guard (`_check_manager_access`)
Verifies if `self.env.user` belongs to `reserve_hub.group_reserve_hub_manager` or `reserve_hub.group_reserve_hub_admin`. If not, raises `UserError`.

---

## 3. Workflow Actions API

- `action_submit()`: Transitions record from `draft` to `submitted`.
- `action_approve()`: Checks manager access and transitions record from `submitted` to `approved`, setting `approved_by_id` and `approval_date`.
- `action_reject()`: Checks manager access and transitions record from `submitted` to `rejected`, setting `approved_by_id` and `approval_date`.
- `action_cancel()`: Transitions state to `cancelled` (disabled when state is `done`).
- `action_set_to_draft()`: Resets `cancelled` or `rejected` bookings back to `draft`.
- `action_mark_done()`: Transitions state from `approved` to `done`.

---

## 4. Security & ACL Matrix

### 4.1 Model Permissions (`ir.model.access.csv`)

| Model | Employee (Read / Write / Create / Delete) | Manager (Read / Write / Create / Delete) | Admin (Read / Write / Create / Delete) |
| --- | --- | --- | --- |
| `resource.category` | `1 / 0 / 0 / 0` | `1 / 1 / 1 / 1` | `1 / 1 / 1 / 1` |
| `reserve.resource` | `1 / 0 / 0 / 0` | `1 / 1 / 1 / 1` | `1 / 1 / 1 / 1` |
| `reserve.booking` | `1 / 1 / 1 / 0` | `1 / 1 / 1 / 1` | `1 / 1 / 1 / 1` |

---

## 5. UI Views Overview

1. **Calendar View (`view_reserve_booking_calendar`)**:
   Renders booking events visually on day/week/month grids, color-coded by `resource_id`.
2. **Kanban View (`view_reserve_resource_kanban`)**:
   Presents resource cards with thumbnail images, status badges, location tags, and interactive smart buttons for associated bookings.
3. **Form View with Statusbar (`view_reserve_booking_form`)**:
   Dynamic buttons displayed according to workflow states and user security groups. Read-only fields enforcement when state in `('approved', 'rejected', 'done', 'cancelled')`.
4. **Pivot & Graph Dashboard Views (`view_reserve_booking_pivot`, `view_reserve_booking_graph`)**:
   Aggregates reservation statistics, total hours booked, and status distribution across categories.
