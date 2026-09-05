from django.shortcuts import render

def doctor_list(request):
    return render(request, 'doctors/doctor_list.html')
