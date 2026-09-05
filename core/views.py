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
    hero_images = GalleryImage.objects.all()[:6]
    
    stats = {
        'years': 25,
        'doctors_count': Doctor.objects.filter(is_active=True).count() or 18,
        'departments_count': Department.objects.count() or 6,
        'patients_count': 50000,
    }

    context = {
        'departments': departments,
        'doctors': doctors,
        'testimonials': testimonials,
        'hero_images': hero_images,
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
            
            # Send email notification to admin via console backend
            try:
                subject = f"[Harborlight Hospital] New Inquiry: {contact_msg.subject}"
                body = (
                    f"New patient message submitted via Harborlight Hospital website:\n\n"
                    f"From: {contact_msg.name}\n"
                    f"Email: {contact_msg.email}\n"
                    f"Phone: {contact_msg.phone or 'Not provided'}\n"
                    f"Subject: {contact_msg.subject}\n\n"
                    f"Message:\n{contact_msg.message}\n"
                )
                admin_email = getattr(settings, 'ADMIN_EMAIL', 'admin@harborlighthospital.example')
                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [admin_email],
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
