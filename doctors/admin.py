from django.contrib import admin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        'name', 
        'department', 
        'specialization', 
        'qualification', 
        'experience_years', 
        'available_days', 
        'is_active'
    )
    list_filter = ('department', 'is_active', 'available_days')
    search_fields = ('name', 'specialization', 'qualification', 'bio')
    list_editable = ('is_active',)
