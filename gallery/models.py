from django.db import models

class GalleryImage(models.Model):
    CATEGORY_CHOICES = [
        ('Hospital', 'Hospital'),
        ('Equipment', 'Equipment'),
        ('Events', 'Events'),
        ('Rooms', 'Rooms'),
    ]

    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to='gallery/')
    category = models.CharField(
        max_length=50, 
        blank=True,
        default='Hospital'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'

    def __str__(self):
        return self.title
