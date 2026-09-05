"""
URL configuration for harborlight_hospital project.
Harborlight Multispecialty Hospital - "Compassionate Care, Modern Medicine"
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
    path('departments/', include('departments.urls', namespace='departments')),
    path('doctors/', include('doctors.urls', namespace='doctors')),
    path('gallery/', include('gallery.urls', namespace='gallery')),
    path('appointments/', include('appointments.urls', namespace='appointments')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
