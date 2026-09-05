# 🏥 Harborlight Multispecialty Hospital

> *"Compassionate Care, Modern Medicine"*

A modern, full-featured hospital and healthcare management web platform built with **Django 5.x**, **Bootstrap 5**, and custom branded styling.

---

## 🎨 Brand Identity & Palette

Harborlight Multispecialty Hospital is built around a distinct, professional healthcare brand kit:

| Element | Specification | Hex / Value | Usage |
|---|---|---|---|
| **Site Name** | Harborlight Multispecialty Hospital | — | Header & Brand titles |
| **Tagline** | *"Compassionate Care, Modern Medicine"* | — | Hero & Mission statement |
| **Primary Color** | Deep Medical Sapphire | `#0F3D69` | Primary branding, buttons, headers, footer |
| **Accent Color** | Medical Cerulean | `#0284C7` | Action CTAs, booking buttons, highlights |
| **Background** | Pristine Clinical Slate | `#F8FAFC` | Body background, modern crisp surfaces |
| **Dark Text** | Deep Slate 900 | `#0F172A` | Ultra-readable AAA contrast typography |
| **Support Color** | Clinical Emerald | `#059669` | Health indicators, badges, card accents |
| **Headings Font** | Poppins | Google Fonts | Titles, headers, section titles |
| **Body Font** | Inter | Google Fonts | Body copy, forms, navigation |

### 📍 Hospital Contact Information (Default)
- **Address:** 12 Wellness Avenue, Riverdale, TX 75001
- **Phone:** +1 (555) 010-7890
- **Email:** info@harborlighthospital.example
- **Emergency:** 24/7 Trauma & Outpatient Support

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
├── manage.py                        # Django CLI entrypoint
├── requirements.txt                 # Dependencies specification
├── .env                             # Environment variables
├── .gitignore                       # Ignored cache, venv, and media files
├── README.md                        # Project documentation
│
├── harborlight_hospital/            # Project configuration
│   ├── settings.py                  # Project settings (Apps, WhiteNoise, Crispy)
│   ├── urls.py                      # Root URL router
│   ├── wsgi.py                      # WSGI configuration
│   └── asgi.py                      # ASGI configuration
│
├── core/                            # Public informational pages
│   ├── models.py                    # Testimonial & ContactMessage
│   ├── views.py                     # Home, About, Contact
│   └── urls.py                      # Routes for core pages
│
├── departments/                     # Clinical specialties & services
│   ├── models.py                    # Department & Service
│   ├── views.py                     # Department list & detail
│   └── urls.py
│
├── doctors/                         # Physician roster & profiles
│   ├── models.py                    # Doctor model (department FK, experience)
│   ├── views.py                     # Doctor directory
│   └── urls.py
│
├── gallery/                         # Campus & equipment media
│   ├── models.py                    # GalleryImage (Hospital, Equipment, Events, Rooms)
│   ├── views.py                     # Gallery list
│   └── urls.py
│
├── appointments/                    # Online patient consultation booking
│   ├── models.py                    # Appointment (department, doctor, date/time, status)
│   ├── views.py                     # Booking workflow
│   └── urls.py
│
├── dashboard/                       # Staff & internal hospital portal
│   ├── views.py                     # Staff overview & appointment tracking
│   └── urls.py
│
├── templates/                       # Project template hierarchy
│   ├── base.html                    # Base layout with fonts, CDN, & branding
│   ├── includes/
│   │   ├── navbar.html              # Top bar, branding, & responsive menu
│   │   └── footer.html              # Hospital details, links, & copyright
│   ├── core/                        # home.html, about.html, contact.html
│   ├── departments/                 # department_list.html
│   ├── doctors/                     # doctor_list.html
│   ├── gallery/                     # gallery_list.html
│   ├── appointments/                # book_appointment.html
│   └── dashboard/                   # index.html
│
├── static/                          # Static assets
│   ├── css/style.css                # Brand kit variables & component styles
│   ├── js/main.js                   # Client-side scripts
│   └── images/                      # Static branding images
│
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
pip install -r requirements.txt
```

### 4. Environment Variables
Create a `.env` file at the root:
```env
DEBUG=True
SECRET_KEY=your-secure-secret-key-here
ALLOWED_HOSTS=127.0.0.1,localhost,testserver
```

### 5. Apply Migrations
```powershell
python manage.py migrate
```

### 6. Create Admin Superuser
```powershell
python manage.py createsuperuser
```

### 7. Run the Development Server
```powershell
python manage.py runserver
```

Visit the running application at: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**  
Access the Django Administration panel at: **[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)**

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
| `/dashboard/` | `dashboard:index` | Hospital staff management portal |
| `/admin/` | `admin:index` | Django Admin management |

---

## 🧪 Verification & Testing

Run Django system checks:
```powershell
python manage.py check
```

Collect static files with WhiteNoise:
```powershell
python manage.py collectstatic --noinput
```

---

## 📄 License

This project is licensed under the MIT License.

