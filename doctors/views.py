from django.shortcuts import render, get_object_or_404
from .models import Doctor
from departments.models import Department

def doctor_list(request):
    department_slug = request.GET.get('department', '').strip()
    doctors = Doctor.objects.filter(is_active=True).select_related('department')
    if department_slug and department_slug != 'all':
        doctors = doctors.filter(department__slug=department_slug)

    departments = Department.objects.all()

    context = {
        'doctors': doctors,
        'departments': departments,
        'selected_department_slug': department_slug,
    }
    return render(request, 'doctors/doctor_list.html', context)


def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk, is_active=True)
    department_services = doctor.department.services.all() if doctor.department else []

    context = {
        'doctor': doctor,
        'department_services': department_services,
    }
    return render(request, 'doctors/doctor_detail.html', context)
