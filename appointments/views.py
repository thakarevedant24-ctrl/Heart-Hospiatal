import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings

from .models import Appointment
from .forms import AppointmentForm
from departments.models import Department
from doctors.models import Doctor

def book_appointment(request):
    """
    Handles appointment booking requests.
    Supports deep-link pre-filling via query parameters:
      - ?doctor=<id>
      - ?department=<slug_or_id>
    """
    preselected_doctor = None
    preselected_department = None

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        # Ensure doctor queryset allows all active doctors for validation
        form.fields['doctor'].queryset = Doctor.objects.filter(is_active=True)

        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.status = 'pending'
            appointment.save()

            # Format confirmation email
            ref_code = f"HL-{appointment.id:05d}"
            formatted_date = appointment.preferred_date.strftime('%A, %B %d, %Y')
            formatted_time = appointment.preferred_time.strftime('%I:%M %p')
            doctor_display = (
                f"Dr. {appointment.doctor.name} ({appointment.doctor.specialization})"
                if appointment.doctor else "Any Available Clinical Specialist"
            )

            email_subject = f"Appointment Request Received [{ref_code}] - City Hospital"
            email_body = f"""Dear {appointment.patient_name},

Thank you for choosing City Hospital. We have successfully received your consultation request.

==================================================
APPOINTMENT SUMMARY
==================================================
Reference Number: {ref_code}
Patient Name:     {appointment.patient_name}
Department:       {appointment.department.name}
Doctor:           {doctor_display}
Preferred Date:   {formatted_date}
Preferred Time:   {formatted_time}
Status:           Pending Confirmation

Consultation Reason / Notes:
{appointment.notes if appointment.notes else "None specified"}

==================================================
WHAT HAPPENS NEXT?
==================================================
1. Our clinical triage coordinators will review practitioner schedules and verify your time slot.
2. You will receive an SMS/email confirmation once your consultation is locked into our clinic calendar.
3. On the day of your visit, please arrive 15 minutes early and present your photo ID and health insurance card at the main reception.

Need immediate medical assistance?
Our 24/7 Emergency & Trauma Hotline is available at +1 (555) 010-7890.

Warm regards,
Patient Services Coordination Desk
City Hospital
12 Wellness Avenue, Riverdale, TX 75001
Phone: +1 (555) 010-7890 | Email: info@cityhospital.example
"""
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@cityhospital.example')
            try:
                send_mail(
                    email_subject,
                    email_body,
                    from_email,
                    [appointment.email],
                    fail_silently=True,
                )
            except Exception:
                pass

            messages.success(
                request,
                f"Your appointment request ({ref_code}) was submitted successfully! A confirmation email has been dispatched."
            )
            return redirect('appointments:booking_confirmation', pk=appointment.pk)
        else:
            messages.error(request, "Please review and correct the highlighted errors below.")
    else:
        # Pre-filling logic from GET query params
        initial_data = {}
        doctor_param = request.GET.get('doctor')
        department_param = request.GET.get('department')

        if doctor_param:
            try:
                preselected_doctor = Doctor.objects.filter(id=doctor_param, is_active=True).select_related('department').first()
                if preselected_doctor:
                    preselected_department = preselected_doctor.department
                    initial_data['doctor'] = preselected_doctor.id
                    initial_data['department'] = preselected_doctor.department.id
            except (ValueError, TypeError):
                pass

        if not preselected_department and department_param:
            # Check by slug first, then numeric ID
            dept_obj = Department.objects.filter(slug=department_param).first()
            if not dept_obj and department_param.isdigit():
                dept_obj = Department.objects.filter(id=int(department_param)).first()
            if dept_obj:
                preselected_department = dept_obj
                initial_data['department'] = dept_obj.id

        form = AppointmentForm(initial=initial_data)
        if preselected_department:
            form.fields['doctor'].queryset = Doctor.objects.filter(
                department=preselected_department,
                is_active=True
            ).order_by('name')

    all_departments = Department.objects.all().order_by('name')
    today_str = datetime.date.today().isoformat()

    context = {
        'form': form,
        'preselected_doctor': preselected_doctor,
        'preselected_department': preselected_department,
        'all_departments': all_departments,
        'today_str': today_str,
    }
    return render(request, 'appointments/book_appointment.html', context)


def booking_confirmation(request, pk):
    """
    Renders confirmation receipt with booking reference and preparation checklist.
    """
    appointment = get_object_or_404(
        Appointment.objects.select_related('department', 'doctor'),
        pk=pk
    )
    ref_code = f"HL-{appointment.id:05d}"
    return render(request, 'appointments/booking_confirmation.html', {
        'appointment': appointment,
        'ref_code': ref_code,
    })


def get_doctors_api(request):
    """
    JSON endpoint to return active doctors filtered by department.
    Accepts:
      - ?department_id=<int>
      - ?department_slug=<str>
      - ?department=<slug_or_id>
    """
    dept_id = request.GET.get('department_id')
    dept_slug = request.GET.get('department_slug') or request.GET.get('department')

    qs = Doctor.objects.filter(is_active=True)

    if dept_id and dept_id.isdigit():
        qs = qs.filter(department_id=int(dept_id))
    elif dept_slug:
        if dept_slug.isdigit():
            qs = qs.filter(department_id=int(dept_slug))
        else:
            qs = qs.filter(department__slug=dept_slug)

    qs = qs.order_by('name')

    data = [
        {
            'id': doctor.id,
            'name': doctor.name,
            'specialization': doctor.specialization,
            'qualification': doctor.qualification,
            'available_days': doctor.available_days,
        }
        for doctor in qs
    ]
    return JsonResponse({'doctors': data})
