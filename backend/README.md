# ⚙️ Backend Server Layer — City Heart Hospital

This directory contains all server-side logic, database models, business workflows, configuration settings, and API/view handlers for City Heart Hospital.

---

## 📁 Directory Structure

```text
backend/
├── README.md               # Backend architecture and usage guide
├── manage.py               # Backend command-line management utility
├── requirements.txt        # Server dependencies and libraries
├── .env                    # Environment variables (DEBUG, SECRET_KEY, ALLOWED_HOSTS)
├── db.sqlite3              # SQLite database storage
├── city_hospital/          # Project configuration package
│   ├── settings.py         # App configuration, middleware, database, template paths
│   ├── urls.py             # Root URL routing table
│   ├── wsgi.py             # WSGI web entrypoint
│   └── asgi.py             # ASGI asynchronous entrypoint
├── core/                   # Home, About, Contact views, testimonials, and contact inquiries
├── departments/            # Cardiac division models, views, and URL routing
├── doctors/                # Physician directory, profiles, and availability
├── gallery/                # Facility images, procedure photography, and categories
└── appointments/           # Patient appointment scheduling engine and validations
```

---

## 🚀 Common Commands

### 1. Run Local Development Server
```bash
python manage.py runserver
```

### 2. Apply Database Migrations
```bash
python manage.py migrate
```

### 3. Create New Migrations
```bash
python manage.py makemigrations
```

### 4. Run Test Suite
```bash
python manage.py test
```

### 5. Collect Static Files (Production)
```bash
python manage.py collectstatic --no-input
```

---

## 🔒 Configuration & Security

- **Settings Module**: `city_hospital.settings`
- **Environment Handling**: Managed via `python-decouple` reading `backend/.env`.
- **Allowed Hosts**: Supports localhost (`127.0.0.1`, `localhost`, `testserver`) and production Render domains (`.onrender.com`).
- **CSRF**: Pre-configured with trusted origins for development and Render HTTPS domains.
