from django.shortcuts import render
from departments.models import Department
from doctors.models import Doctor
from core.models import Testimonial

def home(request):
    departments = Department.objects.all()[:6]
    doctors = Doctor.objects.filter(is_active=True).select_related('department')[:8]
    testimonials = Testimonial.objects.filter(is_approved=True)[:6]
    
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
        'stats': stats,
    }
    return render(request, 'core/home.html', context)

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')
