# 🎨 Frontend Presentation Layer — City Heart Hospital

This directory encapsulates the complete presentation and user-interface layer for the City Heart Hospital web platform.

---

## 📁 Directory Structure

```text
frontend/
├── README.md               # Frontend architecture and usage documentation
├── static/                 # Static web assets
│   ├── css/
│   │   └── style.css       # Design system, CSS variables, layout, components, and animations
│   ├── images/
│   │   ├── city-og-banner.svg  # OpenGraph and Twitter social share graphic
│   │   └── favicon.svg         # SVG brand favicon
│   └── js/
│       └── main.js         # Core UI interactions (scroll reveals, stats counter, lightbox, hamburger)
└── templates/              # Django & HTML5 templates
    ├── base.html           # Master layout template (head, meta, navigation, footer, scripts)
    ├── includes/
    │   ├── navbar.html     # Header with contact top-bar & responsive mobile navigation
    │   └── footer.html     # 4-column footer with quick links and emergency contact info
    ├── core/
    │   ├── home.html       # Hero slider, statistics, emergency facilities, preview sections
    │   ├── about.html      # Mission, history timeline, core values, accreditations
    │   └── contact.html    # Inquiry form, direct cardiac hotline, Google Maps embed
    ├── departments/
    │   ├── department_list.html    # Interactive cardiac divisions catalog
    │   └── department_detail.html  # Specialty procedures, clinical team, direct booking
    ├── doctors/
    │   ├── doctor_list.html        # Medical faculty directory with specialty filter tabs
    │   └── doctor_detail.html      # Physician credentials, bio, and booking link
    ├── gallery/
    │   └── gallery_list.html       # Categorized clinical facilities gallery with lightbox
    └── appointments/
        ├── book_appointment.html   # Patient scheduling form with live doctor dropdown
        └── booking_confirmation.html # Printable ticket receipt with CHH reference code
```

---

## 🎨 Design System & Styling Guidelines

- **Primary Colors**:
  - Deep Teal (`#0E5F5C`) &mdash; Primary brand tone.
  - Warm Coral (`#FF6F59`) &mdash; Call-to-action buttons and urgent accents.
  - Soft Cream (`#FAF7F2`) &mdash; Clean, clinical backgrounds.
  - Charcoal Slate (`#26333D`) &mdash; Readable body text tokens.
  - Sage Accent (`#8FB996`) &mdash; Status badges and subtle borders.
- **Typography**:
  - Headings: `Poppins`, sans-serif.
  - Body: `Inter`, sans-serif.
- **Components**:
  - Rounded pill buttons with interactive hover elevations.
  - Border cards with 12px radius and subtle drop shadows.
  - Mobile-responsive navigation (< 768px).

---

## ⚡ Client-Side Interactions (`main.js`)

1. **IntersectionObserver Scroll Reveal**: Animates sections with `.reveal-on-scroll` into view.
2. **Animated Stats Counter**: Counts up dynamically when stats enter the viewport.
3. **Vanilla Lightbox Modal**: Image zoom with keyboard (`Esc`, arrows) and touch navigation.
4. **Hero Slideshow**: Dynamic auto-playing cardiac hero slideshow with navigation controls.
5. **Back to Top Button**: Smooth scroll-to-top triggered after 280px scroll depth.

