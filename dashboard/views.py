from django.shortcuts import redirect

def index(request):
    """
    Redirects to standard Django admin.
    """
    return redirect('/admin/')
