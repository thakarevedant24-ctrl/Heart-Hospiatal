from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from departments.models import Department
from doctors.models import Doctor
from core.models import Testimonial
from gallery.models import GalleryImage

def home(request):
    departments = Department.objects.all()[:6]
    doctors = Doctor.objects.filter(is_active=True).select_related('department')[:8]
    testimonials = Testimonial.objects.filter(is_approved=True)[:6]
    
    cath_img = GalleryImage.objects.filter(title__icontains='Catheterization').first()
    ctvs_img = GalleryImage.objects.filter(title__icontains='Cardiothoracic').first()
    campus_img = GalleryImage.objects.filter(title__icontains='Campus').first() or GalleryImage.objects.filter(title__icontains='Pavilion').first()

    cath_url = cath_img.image.url if (cath_img and cath_img.image) else '/media/gallery/heart_hospital_cath_lab.jpg'
    ctvs_url = ctvs_img.image.url if (ctvs_img and ctvs_img.image) else '/media/gallery/heart_hospital_ctvs_surgery.jpg'
    campus_url = campus_img.image.url if (campus_img and campus_img.image) else '/media/gallery/heart_hospital_main_campus.jpg'

    hero_slides = [
        {
            'image_url': cath_url,
            'title': 'World-Class Heart & Cardiovascular Care',
            'subtitle': 'Dedicated exclusively to advanced interventional cardiology, beating-heart bypass surgery, and 24/7 acute chest pain emergencies.',
            'primary_btn_text': 'Book Cardiac Consultation',
            'primary_btn_url': '/book/',
            'secondary_btn_text': 'Cardiac Divisions',
            'secondary_btn_url': '/departments/',
        },
        {
            'image_url': ctvs_url,
            'title': 'Pioneering Cardiothoracic Surgery & Catheterization',
            'subtitle': 'State-of-the-art hybrid Cath Labs, minimally invasive valve replacements (TAVR), and 3D arrhythmia mapping guided by senior heart specialists.',
            'primary_btn_text': 'Cardiac Procedures',
            'primary_btn_url': '/departments/',
            'secondary_btn_text': 'Meet Heart Specialists',
            'secondary_btn_url': '/doctors/',
        },
        {
            'image_url': campus_url,
            'title': '24/7 Chest Pain & Acute STEMI Emergency Center',
            'subtitle': 'Rapid door-to-balloon angioplasty in under 45 minutes, Mobile Cardiac ICU ambulances, and round-the-clock intensive cardiac care.',
            'primary_btn_text': 'Emergency Hotline',
            'primary_btn_url': '/contact/',
            'secondary_btn_text': 'About Heart Hospital',
            'secondary_btn_url': '/about/',
        },
    ]

    stats = {
        'years': 25,
        'doctors_count': Doctor.objects.filter(is_active=True).count() or 6,
        'departments_count': Department.objects.count() or 6,
        'patients_count': 50000,
    }

    context = {
        'departments': departments,
        'doctors': doctors,
        'testimonials': testimonials,
        'hero_slides': hero_slides,
        'stats': stats,
    }
    return render(request, 'core/home.html', context)


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_msg = form.save()
            
            # Send email notification to hospital staff via console backend
            try:
                subject = f"[City Heart Hospital] New Inquiry: {contact_msg.subject}"
                body = (
                    f"New patient message submitted via City Heart Hospital website:\n\n"
                    f"From: {contact_msg.name}\n"
                    f"Email: {contact_msg.email}\n"
                    f"Phone: {contact_msg.phone or 'Not provided'}\n"
                    f"Subject: {contact_msg.subject}\n\n"
                    f"Message:\n{contact_msg.message}\n"
                )
                hospital_email = getattr(settings, 'HOSPITAL_EMAIL', 'info@cityhearthospital.example')
                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [hospital_email],
                    fail_silently=True,
                )
            except Exception:
                pass

            messages.success(
                request,
                f"Thank you, {contact_msg.name}! Your message has been sent successfully. Our patient care team will reach out to you shortly."
            )
            return redirect('core:contact')
        else:
            messages.error(request, "Please correct the highlighted errors in the form.")
    else:
        form = ContactForm()

    context = {
        'form': form,
    }
    return render(request, 'core/contact.html', context)
