from django.shortcuts import render

def book_appointment(request):
    return render(request, 'appointments/book_appointment.html')
