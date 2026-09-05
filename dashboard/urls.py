from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_index, name='index'),
    path('appointments/<int:pk>/status/', views.update_appointment_status, name='update_appointment_status'),
    path('messages/<int:pk>/mark-read/', views.mark_message_read, name='mark_message_read'),
]
