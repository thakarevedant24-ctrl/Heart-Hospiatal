from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'patient_name',
        'phone',
        'department',
        'doctor',
        'preferred_date',
        'preferred_time',
        'status',
        'created_at'
    )
    list_filter = ('status', 'department', 'preferred_date', 'created_at')
    search_fields = ('patient_name', 'email', 'phone', 'notes')
    list_editable = ('status',)
