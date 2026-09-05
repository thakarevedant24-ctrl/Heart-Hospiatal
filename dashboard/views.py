import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import AdminLoginForm
from appointments.models import Appointment
from core.models import ContactMessage
from doctors.models import Doctor
from departments.models import Department, Service
from gallery.models import GalleryImage


def admin_login_view(request):
    """
    Branded administrative login view.
    Redirects to dashboard once authenticated.
    """
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    if request.method == 'POST':
        form = AdminLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}! You are logged into the Admin Portal.")
            next_url = request.GET.get('next') or request.POST.get('next') or 'dashboard:index'
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password. Please verify your credentials.")
    else:
        form = AdminLoginForm(request)

    return render(request, 'dashboard/login.html', {'form': form})


def admin_logout_view(request):
    """
    Logs the user out and redirects to the login screen.
    """
    logout(request)
    messages.info(request, "You have been logged out of the Admin Portal.")
    return redirect('admin_login')


@login_required
def dashboard_index(request):
    """
    Hospital Admin Dashboard view showing operational metrics,
    pending appointments, recent inquiries, and quick management links.
    """
    today = timezone.localdate()
    start_week = today - datetime.timedelta(days=today.weekday())
    end_week = start_week + datetime.timedelta(days=6)

    # Operational metrics
    appointments_today_count = Appointment.objects.filter(preferred_date=today).count()
    appointments_week_count = Appointment.objects.filter(
        preferred_date__gte=start_week,
        preferred_date__lte=end_week
    ).count()

    pending_appointments = (
        Appointment.objects.filter(status='pending')
        .select_related('department', 'doctor')
        .order_by('preferred_date', 'preferred_time')
    )
    pending_appointments_count = pending_appointments.count()

    unread_messages_count = ContactMessage.objects.filter(is_read=False).count()
    recent_messages = ContactMessage.objects.all().order_by('-created_at')[:6]

    # Quick links statistics
    doctors_count = Doctor.objects.count()
    services_count = Service.objects.count()
    departments_count = Department.objects.count()
    gallery_count = GalleryImage.objects.count()
    total_appointments_count = Appointment.objects.count()

    context = {
        'today': today,
        'appointments_today_count': appointments_today_count,
        'appointments_week_count': appointments_week_count,
        'pending_appointments_count': pending_appointments_count,
        'unread_messages_count': unread_messages_count,
        'pending_appointments': pending_appointments,
        'recent_messages': recent_messages,
        'doctors_count': doctors_count,
        'services_count': services_count,
        'departments_count': departments_count,
        'gallery_count': gallery_count,
        'total_appointments_count': total_appointments_count,
    }
    return render(request, 'dashboard/index.html', context)


@login_required
@require_POST
def update_appointment_status(request, pk):
    """
    Updates appointment status to 'confirmed' or 'cancelled'.
    Supports both asynchronous AJAX calls and standard form POST requests.
    """
    appointment = get_object_or_404(Appointment, pk=pk)
    action = request.POST.get('action')

    if action == 'confirm':
        appointment.status = 'confirmed'
    elif action == 'cancel':
        appointment.status = 'cancelled'
    else:
        return HttpResponseBadRequest("Invalid status action specified.")

    appointment.save()

    is_ajax = (
        request.headers.get('x-requested-with') == 'XMLHttpRequest' or
        'application/json' in request.headers.get('accept', '')
    )

    if is_ajax:
        return JsonResponse({
            'success': True,
            'id': appointment.id,
            'status': appointment.status,
            'status_display': appointment.get_status_display(),
            'message': f"Appointment #{appointment.id} ({appointment.patient_name}) {appointment.get_status_display().lower()}."
        })

    messages.success(
        request,
        f"Appointment #{appointment.id} ({appointment.patient_name}) has been marked as {appointment.get_status_display()}."
    )
    return redirect('dashboard:index')


@login_required
@require_POST
def mark_message_read(request, pk):
    """
    Marks a contact inquiry as read.
    Supports both AJAX and standard form POST requests.
    """
    contact_msg = get_object_or_404(ContactMessage, pk=pk)
    contact_msg.is_read = True
    contact_msg.save()

    is_ajax = (
        request.headers.get('x-requested-with') == 'XMLHttpRequest' or
        'application/json' in request.headers.get('accept', '')
    )

    if is_ajax:
        return JsonResponse({
            'success': True,
            'id': contact_msg.id,
            'message': f"Inquiry from {contact_msg.name} marked as read."
        })

    messages.success(request, f"Inquiry from {contact_msg.name} marked as read.")
    return redirect('dashboard:index')
