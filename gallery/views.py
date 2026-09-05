from django.shortcuts import render

def gallery_list(request):
    return render(request, 'gallery/gallery_list.html')
