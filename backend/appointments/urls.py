from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.book_appointment, name='book_appointment'),
    path('confirmation/<int:pk>/', views.booking_confirmation, name='booking_confirmation'),
    path('api/doctors/', views.get_doctors_api, name='api_doctors'),
]
