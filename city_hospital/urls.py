"""
URL configuration for city_hospital project.
City Heart Hospital — Mumbai - "Advanced Cardiology & Cardiothoracic Surgery"
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from appointments import views as appointment_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
    path('departments/', include('departments.urls', namespace='departments')),
    path('doctors/', include('doctors.urls', namespace='doctors')),
    path('gallery/', include('gallery.urls', namespace='gallery')),
    path('appointments/', include('appointments.urls', namespace='appointments')),
    path('book/', appointment_views.book_appointment, name='book_alias'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
