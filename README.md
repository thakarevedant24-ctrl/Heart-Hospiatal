# 🫀 City Heart Hospital — Mumbai

> *"Advanced Cardiology & Cardiothoracic Surgery"*

A modern, full-featured web application for an exclusive **Heart Specialty Hospital** located at **Bandra Kurla Complex (BKC), Mumbai**, built with **Django 5.x**, **Bootstrap 5**, and responsive clinical UI.

---

## 🎨 Brand Identity & Palette

City Heart Hospital is built around a distinct, professional healthcare brand kit:

| Element | Specification | Hex / Value | Usage |
|---|---|---|---|
| **Site Name** | City Heart Hospital | — | Header & Brand titles |
| **Tagline** | *"Advanced Cardiology & Cardiothoracic Surgery"* | — | Hero & Mission statement |
| **Primary Color** | Deep Medical Teal | `#0E5F5C` | Primary branding, buttons, headers, footer |
| **Accent Color** | Medical Cerulean | `#0284C7` | Action CTAs, booking buttons, highlights |
| **Background** | Pristine Clinical Slate | `#F8FAFC` | Body background, modern crisp surfaces |
| **Dark Text** | Deep Slate 900 | `#0F172A` | Ultra-readable AAA contrast typography |
| **Support Color** | Clinical Emerald | `#059669` | Health indicators, badges, card accents |
| **Headings Font** | Poppins | Google Fonts | Titles, headers, section titles |
| **Body Font** | Inter | Google Fonts | Body copy, forms, navigation |

### 📍 Hospital Contact Information (Default)
- **Address:** 12 Heart Institute Marg, BKC, Bandra East, Mumbai, Maharashtra 400051
- **Phone:** +91XXXXXXXX50
- **Email:** info@cityhearthospital.example
- **Emergency:** 24/7 Chest Pain & Acute STEMI Emergency Center

---

## 🛠️ Tech Stack

- **Backend:** Python 3.14+ / Django 5.x
- **Frontend:** Django Templates, Bootstrap 5, Bootstrap Icons, Vanilla JavaScript
- **Forms:** `django-crispy-forms` + `crispy-bootstrap5`
- **Static Files:** WhiteNoise (`CompressedManifestStaticFilesStorage`)
- **Media & Images:** Pillow
- **Environment Management:** `python-decouple`
- **Database:** SQLite (Default for development) / PostgreSQL ready

---

## 📁 Project Structure

```text
hospital_website/
├── README.md                        # Project documentation
├── .gitignore                       # Ignored cache, venv, and media files
│
├── backend/                         # 🧠 Python & Django Backend
│   ├── manage.py                    # Backend CLI runner
│   ├── db.sqlite3                   # Database file
│   ├── requirements.txt             # Backend dependencies
│   ├── .env                         # Backend environment configuration
│   │
│   ├── city_hospital/               # Project core configuration
│   │   ├── settings.py              # Settings (Apps, WhiteNoise, Crispy, Paths)
│   │   ├── urls.py                  # Root URL router
│   │   ├── wsgi.py                  # WSGI server configuration
│   │   └── asgi.py                  # ASGI configuration
│   │
│   ├── core/                        # Public informational pages (models, views, forms, tests)
│   ├── departments/                 # Clinical specialties & services (models, views, tests)
│   ├── doctors/                     # Physician roster & profiles (models, views, tests)
│   ├── gallery/                     # Campus & equipment media (models, views, tests)
│   └── appointments/                # Patient consultation booking (models, views, forms, tests)
│
├── frontend/                        # 🎨 Frontend Presentation Layer
│   ├── templates/                   # Semantic HTML5 & Django templates
│   │   ├── base.html                # Base layout with fonts, CDN, & branding
│   │   ├── includes/                # Partial components (navbar.html, footer.html)
│   │   ├── core/                    # home.html, about.html, contact.html
│   │   ├── departments/             # department_list.html, department_detail.html
│   │   ├── doctors/                 # doctor_list.html, doctor_detail.html
│   │   ├── gallery/                 # gallery_list.html
│   │   └── appointments/            # book_appointment.html, booking_confirmation.html
│   │
│   └── static/                      # Static assets
│       ├── css/style.css            # Medical brand design system
│       ├── js/main.js               # Client-side scripts & AJAX
│       └── images/                  # Favicons, SVGs, and branding graphics
│
├── staticfiles/                     # WhiteNoise compiled & compressed static assets
└── media/                           # User-uploaded doctor photos & gallery files
```

---

## 🗄️ Database Models

### 1. `Department` (`departments` app)
- `name`: Specialty name (unique)
- `slug`: Auto-generated from name via `slugify`
- `icon`: Bootstrap icon class (`bi-heart-pulse`)
- `short_description`: Summary for cards
- `full_description`: In-depth clinical service overview

### 2. `Service` (`departments` app)
- `title`: Clinical service title
- `department`: ForeignKey to `Department` (nullable)
- `icon`: Icon class
- `short_description`: Description

### 3. `Doctor` (`doctors` app)
- `name`: Physician name
- `photo`: Image upload (`doctors/`)
- `department`: ForeignKey to `Department`
- `specialization`: Clinical focus area
- `qualification`: Degrees & certifications (e.g. `MD, FACC`)
- `experience_years`: Years of clinical practice
- `bio`: Physician background
- `available_days`: Consultation schedule (e.g. `"Mon-Fri"`)
- `is_active`: Availability toggle

### 4. `GalleryImage` (`gallery` app)
- `title`: Photo title
- `image`: Image upload (`gallery/`)
- `category`: `Hospital`, `Equipment`, `Events`, `Rooms`
- `uploaded_at`: Auto timestamp

### 5. `Testimonial` (`core` app)
- `patient_name`: Patient name
- `message`: Patient review
- `rating`: 1 to 5 stars (validated)
- `photo`: Optional patient photo (`testimonials/`)
- `is_approved`: Moderation toggle

### 6. `ContactMessage` (`core` app)
- `name`, `email`, `phone`, `subject`, `message`
- `created_at`: Submission timestamp
- `is_read`: Staff review status

### 7. `Appointment` (`appointments` app)
- `patient_name`, `email`, `phone`
- `department`: ForeignKey to `Department`
- `doctor`: ForeignKey to `Doctor` (optional)
- `preferred_date`: DateField
- `preferred_time`: TimeField
- `notes`: Medical concern or symptoms
- `status`: `pending`, `confirmed`, `cancelled` (default: `pending`)
- `created_at`: Auto timestamp

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.14)
- Git

### 2. Setup Virtual Environment
```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Or Windows Command Prompt
.venv\Scripts\activate.bat

# Or Linux / macOS
source .venv/bin/activate
```

### 3. Install Dependencies
```powershell
pip install -r backend/requirements.txt
```

### 4. Apply Migrations
```powershell
python backend/manage.py migrate
```

### 5. Run the Development Server
```powershell
python backend/manage.py runserver
# Or navigate to backend:
cd backend
python manage.py runserver
```

Visit the running application at: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🌐 Application URL Endpoints

| URL Route | View | Description |
|---|---|---|
| `/` | `core:home` | Hospital home page & overview |
| `/about/` | `core:about` | About the hospital & mission |
| `/contact/` | `core:contact` | Contact details & inquiry form |
| `/departments/` | `departments:department_list` | Clinical specialties list |
| `/doctors/` | `doctors:doctor_list` | Medical faculty roster |
| `/gallery/` | `gallery:gallery_list` | Facilities & campus photo gallery |
| `/appointments/` | `appointments:book_appointment` | Patient appointment booking |

---

## 🧪 Verification & Testing

Run Django system checks:
```powershell
python backend/manage.py check
```

Run test suite (15 unit tests):
```powershell
python backend/manage.py test
```

Collect static files with WhiteNoise:
```powershell
python backend/manage.py collectstatic --noinput
```

---

## 📄 License

This project is licensed under the MIT License.

