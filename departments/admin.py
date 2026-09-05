from django.contrib import admin
from .models import Department, Service

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon', 'short_description')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'short_description', 'full_description')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'icon', 'short_description')
    list_filter = ('department',)
    search_fields = ('title', 'short_description')
