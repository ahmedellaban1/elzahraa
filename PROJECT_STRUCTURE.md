# Elzahraa — Project Structure

Django clinic management system for **عيادات الزهراء** (Elzahraa Clinics). Arabic RTL UI with role-based access for admin, doctor, receptionist, and patient.

**Stack:** Django 5.2 · SQLite (dev) · Bootstrap 5 RTL · Font Awesome 7 · Cairo font · `Africa/Cairo` timezone

---

## Root layout

```
elzahraa/
├── manage.py                 # Django CLI entry point
├── requirements.txt          # Python dependencies
├── db.sqlite3                # Local SQLite database
├── .gitignore
│
├── core/                     # Project config (settings, root URLs, WSGI/ASGI)
├── etc/                      # Shared constants (choice tuples)
│
├── accounts/                 # Custom user, login, profile, role signals
├── patients/                 # Patient records
├── staff/                    # Doctors & receptionists
├── appointments/             # Appointments & prescriptions
├── services/                 # Clinic services & service records
├── medicines/                # Medicine catalog
├── dashboard/                # Admin dashboard, search, discounts, expenses
│
├── templates/                # Global templates (base + error pages)
├── static/                   # CSS, fonts, vendor JS, icon sets
├── media/                    # User uploads (gitignored; created at runtime)
└── venv/                     # Local virtualenv (gitignored)
```

---

## Apps

| App | Role |
|-----|------|
| `core` | Project package: settings, root URL routing, WSGI/ASGI |
| `etc` | Shared choice constants used by models across apps |
| `accounts` | `CustomUser` (`AUTH_USER_MODEL`), auth views, profile auto-creation |
| `patients` | Patient profile linked 1:1 to a user |
| `staff` | Doctor (exam type + revenue split) and receptionist |
| `appointments` | Bookings, daily queue number, prescriptions |
| `services` | Service catalog and billed service records |
| `medicines` | Medicine catalog for prescriptions |
| `dashboard` | Admin stats, Excel export, unified search, discounts, expenses |

URL prefixes (from `core/urls.py`):

| Prefix | App |
|--------|-----|
| `/` | `dashboard` |
| `/accounts/` | `accounts` |
| `/appointments/` | `appointments` |
| `/staff/` | `staff` |
| `/patients/` | `patients` |
| `/services/` | `services` |
| `/medicines/` | `medicines` |
| `/admin/` | Django admin |
| `/summernote/` | django-summernote |
| `/__debug__/` | debug toolbar (DEBUG only) |

Auth: login → `accounts:login`; after login → `dashboard:dashboard_router` (admin / doctor / receptionist / patient).

---

## Domain model

```
CustomUser (role: admin | doctor | receptionist | patient)
    │
    ├── 1:1 Patient
    ├── 1:1 Doctor ──┬── * Appointment ── * PrescriptionItem ── Medicine
    └── 1:1 Receptionist   └── * ServiceRecord ── Service

Appointment ── 1:1 DiscountRecord
ServiceRecord ── 1:1 DiscountRecord
Expense (clinic operating costs, standalone)
```

Revenue on appointments and service records is split into `doctor_money` and `clinic_money`. Doctors use either **percentage** or **time-share** (`examination_type`).

---

## `core/` — project config

```
core/
├── __init__.py
├── settings.py      # Apps, DB, AUTH_USER_MODEL, static/media, login URLs
├── urls.py          # Root urlpatterns
├── wsgi.py
└── asgi.py
```

Notable settings: `AUTH_USER_MODEL = accounts.CustomUser`, `LANGUAGE_CODE = en-us` with Arabic UI in templates, `TIME_ZONE = Africa/Cairo`, SQLite at `db.sqlite3`.

---

## `etc/` — shared choices

```
etc/
└── choices.py
```

Central tuples: user roles, gender, examination type, appointment status/type, medicine dosage/frequency/route, discount types, expense categories. Labels are in Arabic.

---

## `accounts/`

```
accounts/
├── models.py        # CustomUser (role, phone, gender, created_by)
├── views.py         # login, logout, profile
├── urls.py
├── admin.py
├── signals.py       # On user create: Patient/Doctor/Receptionist + permission group
├── apps.py          # Loads signals in ready()
├── tests.py
├── migrations/
└── templates/accounts/
    ├── login.html
    ├── logout.html
    └── profile.html
```

Roles: `admin`, `doctor`, `receptionist`, `patient`. Groups: `admin_permissions`, `doctor_permissions`, `receptionist_permissions`, `patient_permissions`.

**URLs:** `login/` · `logout/` · `profile/`

---

## `patients/`

```
patients/
├── models.py        # Patient (user, address, birth_date, notes)
├── views.py         # get_patient (JSON), create, detail, reset password
├── forms.py         # PatientCreationForm
├── urls.py
├── admin.py
├── tests.py
├── migrations/
└── templates/patients/
    ├── create_patient.html
    └── patient_detail.html
```

**URLs:** `get-patient/` · `create-patient/` · `<pk>/` · `<pk>/reset-password/`

---

## `staff/`

```
staff/
├── models.py        # Doctor, Receptionist
├── views.py         # dashboards, CRUD doctor, create receptionist, Excel export
├── forms.py         # DoctorCreationForm, DoctorUpdateForm, ReceptionistCreationForm
├── urls.py
├── admin.py
├── tests.py
├── migrations/
└── templates/staff/
    ├── doctor_dashboard.html
    ├── create_doctor.html
    ├── update_doctor.html
    ├── doctor_detail.html
    └── create_receptionist.html
```

`Doctor`: specialization, `examination_type` (percentage | time_share), `percentage_value` / `price_value`.  
`Receptionist`: salary, hire_date.

**URLs:** `get-doctor/` · `dashboard/` · `create-doctor/` · `create-receptionist/` · `doctor/<pk>/` · `doctor/<pk>/edit/` · `doctor/<pk>/export-excel/` · `doctor/<pk>/reset-password/`

---

## `appointments/`

```
appointments/
├── models.py        # Appointment, PrescriptionItem
├── views.py         # list/create/update, status, prescription, print, notes
├── forms.py         # AppointmentForm
├── urls.py
├── admin.py
├── tests.py
├── migrations/
└── templates/appointments/
    ├── index.html
    ├── update_appointment.html
    ├── add_prescription.html
    ├── print_prescription.html
    └── partials/appointment_table.html
```

`Appointment` auto-assigns `session_number` (daily queue per doctor). Status: pending / confirmed / completed / cancelled. Type: examination / follow-up.

**URLs:** `` · `list/` · `create/` · `update/<pk>/` · `update-status/<pk>/` · `prescription/<id>/` · `prescription/<id>/print/` · `prescription/<id>/save-notes/`

---

## `services/`

```
services/
├── models.py        # Service (catalog), ServiceRecord (billed instance)
├── views.py         # catalog CRUD, add record, JSON list
├── forms.py         # ServiceForm, ServiceRecordForm
├── urls.py
├── admin.py
├── tests.py
├── migrations/
└── templates/services/
    ├── service_list.html
    ├── service_detail.html
    ├── create_service.html
    ├── update_service.html
    ├── add_service.html
    └── update_service_record.html
```

**URLs:** `` (list) · `define-service/` · `add-service/` · `add-service/<patient_id>/` · `get-services/` · `<pk>/` · `<pk>/edit/` · `<pk>/delete/` · `record/<pk>/edit/` · `record/<pk>/delete/`

---

## `medicines/`

```
medicines/
├── models.py        # Medicine (trade/scientific name, concentration)
├── views.py         # list, add, edit, toggle active, search
├── urls.py
├── admin.py
├── tests.py
├── migrations/
└── templates/medicines/
    ├── list_medicines.html
    ├── add_medicine.html
    └── edit_medicine.html
```

**URLs:** `` · `add/` · `<pk>/edit/` · `<pk>/toggle/` · `search/`

---

## `dashboard/`

```
dashboard/
├── models.py        # DiscountRecord, Expense
├── views.py         # router, admin stats, search, Excel, discounts, expenses
├── urls.py
├── admin.py
├── tests.py
├── migrations/
└── templates/dashboard/
    ├── admin_dashboard.html
    ├── unified_search.html
    ├── add_discount.html
    └── manage_expenses.html
```

`dashboard_router` sends users by role:

- admin / superuser → admin dashboard  
- doctor → staff doctor dashboard  
- receptionist → appointments index  
- other → profile  

**URLs:** `` · `admin-dashboard/` · `export-excel/` · `search/` · `discount/appointment/<pk>/` · `discount/service/<pk>/` · `expenses/` · `expenses/<pk>/delete/`

---

## Templates & static

```
templates/
├── base.html        # RTL layout, navbar by role, Bootstrap + FA + Cairo
├── 403.html
├── 404.html
└── 500.html
```

App templates live under each app’s `templates/<app>/` (Django `APP_DIRS`).

```
static/
├── css/
│   ├── style.css
│   └── fonts/cairo/          # Cairo variable + static TTF weights
├── bootstrap-5.3.8-dist/
├── fontawesome-free-7.2.0-web/
├── vendor/
│   ├── flatpickr/            # Date picker (dark.css)
│   └── tom-select/           # Searchable selects
└── voice/                    # Placeholder (empty)
```

`STATICFILES_DIRS = [BASE_DIR / 'static']` · `MEDIA_ROOT = BASE_DIR / 'media'`

---

## Permissions

Views use `@login_required` and Django `@permission_required` (e.g. `appointments.add_appointment`, `services.view_service`). Groups are attached in `accounts/signals.py` when a user is created.

---

## Dependencies (`requirements.txt`)

| Package | Use |
|---------|-----|
| Django 5.2 | Framework |
| mysqlclient | MySQL driver (optional prod DB) |
| django-debug-toolbar | Dev SQL/request inspector |
| django-extensions | Extra management commands |
| django-filter | Queryset filtering |
| django-summernote | Rich text |
| django-bootstrap5 | Bootstrap form rendering |
| openpyxl | Excel export (admin + doctor reports) |
| bleach | HTML sanitizing |
)
</think>

Created [`PROJECT_STRUCTURE.md`](f:\elzahraa\PROJECT_STRUCTURE.md) at the repo root.

It maps the Django 5.2 clinic app: seven domain apps (`accounts`, `patients`, `staff`, `appointments`, `services`, `medicines`, `dashboard`), models and URLs, role-based routing, and where templates/static live.