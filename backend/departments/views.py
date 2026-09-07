from django.shortcuts import render, get_object_or_404
from .models import Department, Service

def department_list(request):
    departments = Department.objects.all()
    selected_dept_slug = request.GET.get('department', '').strip()

    services = Service.objects.select_related('department').all()
    if selected_dept_slug and selected_dept_slug != 'all':
        services = services.filter(department__slug=selected_dept_slug)

    context = {
        'departments': departments,
        'services': services,
        'selected_dept_slug': selected_dept_slug,
    }
    return render(request, 'departments/department_list.html', context)


def department_detail(request, slug):
    department = get_object_or_404(Department, slug=slug)
    services = department.services.all()
    doctors = department.doctors.filter(is_active=True)

    context = {
        'department': department,
        'services': services,
        'doctors': doctors,
    }
    return render(request, 'departments/department_detail.html', context)
