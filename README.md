# SSGC Customer Registration

A web application to **register and manage SSGC customers**. It is built with **Django** (Python) and **MySQL**, and it lets staff add, view, search, edit and delete customer records from a clean browser interface.

This project was built as an internship task and is also a learning project for Django.

---

## 1. Introduction

SSGC needs a simple place to keep customer registration records: who the customer is, where they live, which zone and region they belong to, their meter details, and the status of their case.

This app does that. A staff member logs in, sees a list of all customers, and can:

- add a new customer,
- open a customer to see every detail,
- edit a customer,
- delete a customer,
- search and browse through many records easily.

In technical words, this is a **CRUD application** (Create, Read, Update, Delete).

---

## 2. Features

| Feature | What it does |
|---|---|
| **Create** | Add a new customer using a form split into clear sections |
| **Read** | A list page with all customers, and a detail page showing every field |
| **Update** | Edit any customer (the Claim ID is locked so it cannot be changed by mistake) |
| **Delete** | Delete a customer after a confirmation screen |
| **Search** | Find customers by name, CNIC or Claim ID |
| **Pagination** | Shows 10 customers per page with Previous and Next buttons |
| **Validation** | Checks CNIC format (`42101-1234567-1`) and phone number format |
| **Login** | All pages need a login. Users are created by an admin |
| **Admin panel** | Django admin at `/admin/` to manage users and fix data |
| **Messages** | Green notes such as "Customer added successfully" |
| **Auto numbering** | `UR_CONSUMER_S_NO` is numbered automatically and renumbered after a delete |
| **Status colors** | Case status shows as a colored badge (Approved, Pending, Rejected) |

---

## 3. Technologies Used

| Part | Technology |
|---|---|
| Language | Python 3.13 |
| Framework | Django 5.2 |
| Database | MySQL 8.0 |
| Database driver | mysqlclient |
| Secrets handling | python-dotenv (`.env` file) |
| Design | Bootstrap 5, Bootstrap Icons, Google Font "Inter" |
| Editor / tools | VS Code, MySQL Workbench |

> **Why Django 5.2 and not 6?** Django 6 needs MySQL 8.4 or newer. This project uses MySQL 8.0, so Django 5.2 (a long-term support version) is used.

---

## 4. Project Structure

```
ssgc_project/
├── manage.py                 Django's command tool
├── requirements.txt          List of Python packages needed
├── database.sql              SQL script to create the database and table
├── README.md                 This file
├── .env                      Private settings (NEVER share or upload)
├── .env.example              Example of the settings, with fake values
├── .gitignore                Files Git must ignore
│
├── config/                   Project-wide settings
│   ├── settings.py           Database, installed apps, login settings
│   └── urls.py               Main address book (admin + app)
│
└── customers/                The main app
    ├── models.py             Describes the customer table in Python
    ├── forms.py              The customer form and validation rules
    ├── views.py              The logic (list, add, edit, delete, detail)
    ├── urls.py               Addresses for the app (login, logout, CRUD)
    ├── admin.py              Registers the model in the admin panel
    ├── templates/customers/  HTML pages
    │   ├── base.html             Shared layout (navbar, styles)
    │   ├── login.html            Login page
    │   ├── customer_list.html    List, search, pagination
    │   ├── customer_form.html    Add / Edit form
    │   ├── customer_detail.html  Full details of one customer
    │   └── customer_confirm_delete.html   Delete confirmation
    └── static/customers/images/  Logo
```

---

## 5. How the App Works (in simple words)

Django follows the **MVT** pattern: Model, View, Template.

| Part | Meaning | File in this project |
|---|---|---|
| **Model** | Describes the database table | `models.py` |
| **View** | The logic that decides what to do | `views.py` |
| **Template** | The HTML page the user sees | `templates/customers/*.html` |

When you open a page, this is what happens:

```
Browser asks for an address (for example /5/edit/)
   -> config/urls.py hands it to customers/urls.py
   -> customers/urls.py picks the matching view
   -> the view talks to the model (MySQL) and uses the form
   -> the view sends data to a template
   -> the template becomes the page you see
```

### Pages and addresses

| Address | What it shows | Action |
|---|---|---|
| `/login/` | Login page | Sign in |
| `/logout/` | Logs you out (button in the navbar) | Sign out |
| `/` | Customer list with search and pages | Read all |
| `/add/` | Empty form | Create |
| `/<claim_id>/` | All details of one customer | Read one |
| `/<claim_id>/edit/` | Form filled with current data | Update |
| `/<claim_id>/delete/` | "Are you sure?" screen | Delete |
| `/admin/` | Django admin panel | Manage users and data |

---

## 6. Database Design

The database is called **`ssgc_db`** and the main table is **`customer_registration`** with **40 columns**.

- **Primary key:** `CLAIM_ID` (unique for every customer).
- **`UR_CONSUMER_S_NO`:** an auto-numbered serial that is also unique. It is renumbered after a delete (see Notes).
- **Required fields (8):** `CLAIM_ID`, `CNIC`, `FULL_NAME`, `UNIT`, `ZONE_NAME`, `SUB_ZONE`, `REGION`, `USERID`. All other fields are optional.

The fields are grouped into sections, which are also the sections shown on the form and detail pages:

| Section | Fields |
|---|---|
| **Identity** | CLAIM_ID, CNIC, NAME_PREFIX, FULL_NAME, PHONE_NUMBER |
| **Address** | ADDRESS1 to ADDRESS4, CITY |
| **Organization** | UNIT, ZONE_NAME, SUB_ZONE, REGION, AREA_CD, BILLING_GRP, AMG |
| **Meter and Billing** | NEAREST_METER_NBR, BULK_METER_NO, SWITCHH, LAST_BM, OVR_VOLUME, OVR_RATE_AMT, PREM_ID, SP_ID |
| **Category and Location** | CATEGORY_CD, CATEGORY_DESCR, LOCATION_ID, LOCATION_DESCR, X_LONGITUDE, Y_LATITUDE |
| **Committee and Case** | COMMITTE_VISIT_DATE, COMMITTE_APPROVED_DATE, COMMITTE_REMARKS, CASE_STATUS, UR_CONSUMER_STATUS_FLG |
| **Audit** | SETUP_DT, USERID, LAST_UPDATED_DT |

The table is created **by hand in MySQL** (using `database.sql`), not by Django migrations. In `models.py` this is why the model has `managed = False`.

---

## 7. Validation Rules

| Field | Rule | Example |
|---|---|---|
| CNIC | 5 digits, dash, 7 digits, dash, 1 digit | `42101-1234567-1` |
| Phone number | Only digits, `+`, `-` and spaces, 7 to 20 characters | `0300-1234567` |
| Claim ID | Up to 19 characters, must be unique | `CLM0000000000000001` |
| Required fields | Cannot be left empty | see Section 6 |
| Dates | Chosen from a calendar picker | `2026-10-01` |

If something is wrong, the form shows a red message under the field.

---

## 8. Setup Guide (Windows)

Follow these steps in order on a new computer.

### Step 1: Install the basics
- Python 3.13
- MySQL Server 8.0 and MySQL Workbench
- VS Code (or any editor)

### Step 2: Get the project and open it
Open the project folder in VS Code and open a terminal in it.

### Step 3: Create and activate a virtual environment
```
python -m venv venv
venv\Scripts\activate
```
You should see `(venv)` at the start of the terminal line. If PowerShell blocks the script, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once.

### Step 4: Install the packages
```
pip install -r requirements.txt
```

### Step 5: Create the database
1. Open `database.sql`.
2. Replace `CHANGE_ME` with a password of your own choice.
3. Run the whole script in MySQL Workbench. It creates the database `ssgc_db`, the table `customer_registration` and a MySQL user `ssgc_user`.

### Step 6: Create the `.env` file
In the project root (next to `manage.py`), create a file named `.env`:

```
DB_NAME=ssgc_db
DB_USER=ssgc_user
DB_PASSWORD=the_password_you_chose_in_step_5
DB_HOST=localhost
DB_PORT=3306
SECRET_KEY=any-long-random-text
DEBUG=True
```

Rules: no spaces around `=`, no quotes. `DB_PASSWORD` must match the password in `database.sql`.

To generate a safe secret key:
```
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### Step 7: Create Django's built-in tables
```
python manage.py migrate
```
This creates the user, session and admin tables. It does not touch `customer_registration`.

### Step 8: Create the first admin user
```
python manage.py createsuperuser
```
Choose a username and a strong password.

### Step 9: Run the server
```
python manage.py runserver
```
Open **http://127.0.0.1:8000/** in your browser. You will be sent to the login page.

---

## 9. How to Use the App

### Log in
Open the site and sign in with a username and password.

### Add a customer
1. Click **New Customer**.
2. Fill the fields. Fields with a red `*` are required.
3. Click **Save**. You will see a green success message.

### Search
Type a name, CNIC or Claim ID in the search box and click **Search**. Click **Clear** to see everyone again.

### View, edit, delete
Use the icons at the end of each row:
- Eye icon: view all details
- Pencil icon: edit
- Trash icon: delete (asks for confirmation first)

### Add users for your colleagues
There is no public sign-up page. Only an admin can create accounts:

1. Open `/admin/` and log in as the admin.
2. Go to **Users**, then **Add user**.
3. Enter a username and password and click **Save**.
4. Make sure **Active** is ticked. Leave **Staff status** and **Superuser status** unticked for normal employees.
5. Give the username and password to the employee. They log in at the normal login page and will see the app, not the admin panel.

To stop someone from using the system, untick **Active** on their account.

---

## 10. Notes and Design Decisions

- **Secrets are kept out of the code.** Passwords and the secret key live in `.env`, and `settings.py` reads them. Never share or upload `.env`.
- **Limited MySQL user.** Django connects as `ssgc_user`, who can only access `ssgc_db`, instead of `root`.
- **Renumbering `UR_CONSUMER_S_NO`.** After a delete, the serial numbers are rebuilt as 1, 2, 3... with no gaps (for example, deleting number 2 turns the old 3 into 2). `CLAIM_ID` is the permanent identifier. If another system ever stores `UR_CONSUMER_S_NO`, those references would change, so it should use `CLAIM_ID` instead.
- **Claim ID is locked when editing**, because it is the primary key. Changing it would create a new record instead of updating the old one.
- **Delete needs a confirmation** and only works through a POST request, so it cannot happen by accidentally opening a link.

---

## 11. Troubleshooting

| Problem | Likely cause and fix |
|---|---|
| `Access denied for user 'ssgc_user'` | Password in `.env` does not match MySQL, or the `.env` file has spaces or quotes |
| `Unknown database 'ssgc_db'` | `database.sql` was not run, or `DB_NAME` is misspelled |
| `Can't connect to MySQL server` | MySQL service is stopped. Start it (`net start MySQL80` as administrator) |
| `MySQL 8.4 or later is required` | Django 6 is installed. Run `pip install "django>=5.2,<5.3"` |
| `No module named 'dotenv'` | Packages not installed, or `(venv)` is not active |
| `TemplateDoesNotExist` | Template file is missing or in the wrong folder (`customers/templates/customers/`) |
| `403 CSRF verification failed` | A form is missing `{% csrf_token %}` |
| Page looks unstyled | No internet. Bootstrap and icons load from the internet |
| Date box empty when editing | Date widgets need `format='%Y-%m-%d'` in `forms.py` |

---

## 12. Known Limitations

- Any logged-in user can add, edit and delete. There are no separate view-only roles yet.
- Renumbering after a delete is not safe if two people delete at the exact same moment.
- Bootstrap and fonts are loaded from the internet, so the pages need a connection to look right.
- No automated tests yet.

## 13. Ideas for Future Improvement

- Role-based permissions (for example, view-only users)
- Export customers to Excel or CSV
- Filters by region, zone and case status
- Automated tests for CRUD and login
- Activity log of who changed what and when
- Deployment on a company server

---

## 14. What I Learned

- Planning a project from the database first
- Django's MVT structure and how a request travels through it
- Connecting Django to an existing MySQL table (`managed = False`)
- Forms, validation, and CSRF protection
- Authentication (login, logout, protected pages)
- Keeping secrets safe with a `.env` file
- Reading error messages and debugging step by step