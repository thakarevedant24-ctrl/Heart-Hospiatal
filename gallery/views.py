from django.shortcuts import render
from .models import GalleryImage

def gallery_list(request):
    images = GalleryImage.objects.all().order_by('-uploaded_at')
    categories = ['All', 'Hospital', 'Equipment', 'Events', 'Rooms']

    context = {
        'images': images,
        'categories': categories,
    }
    return render(request, 'gallery/gallery_list.html', context)
