"""
URL configuration for harborlight_hospital project.
Harborlight Multispecialty Hospital - "Compassionate Care, Modern Medicine"
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from appointments import views as appointment_views
from dashboard import views as dashboard_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
    path('departments/', include('departments.urls', namespace='departments')),
    path('doctors/', include('doctors.urls', namespace='doctors')),
    path('gallery/', include('gallery.urls', namespace='gallery')),
    path('appointments/', include('appointments.urls', namespace='appointments')),
    path('book/', appointment_views.book_appointment, name='book_alias'),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('login/', dashboard_views.admin_login_view, name='admin_login'),
    path('admin-login/', dashboard_views.admin_login_view, name='admin_login_alias'),
    path('staff-login/', dashboard_views.admin_login_view, name='staff_login_alias'),
    path('logout/', dashboard_views.admin_logout_view, name='admin_logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
