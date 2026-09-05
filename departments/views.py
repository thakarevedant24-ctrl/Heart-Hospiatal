from django.shortcuts import render

def department_list(request):
    return render(request, 'departments/department_list.html')
