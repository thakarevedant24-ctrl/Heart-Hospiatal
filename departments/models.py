from django.db import models
from django.utils.text import slugify

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    icon = models.CharField(
        max_length=50, 
        blank=True, 
        default='bi-heart-pulse', 
        help_text="Bootstrap icon class (e.g. bi-heart-pulse, bi-bandaid)"
    )
    short_description = models.CharField(max_length=255)
    full_description = models.TextField()

    class Meta:
        ordering = ['name']
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Department.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Service(models.Model):
    title = models.CharField(max_length=150)
    department = models.ForeignKey(
        Department, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='services'
    )
    icon = models.CharField(
        max_length=50, 
        blank=True, 
        default='bi-check-circle', 
        help_text="Bootstrap icon class"
    )
    short_description = models.TextField()

    class Meta:
        ordering = ['title']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        if self.department:
            return f"{self.title} ({self.department.name})"
        return self.title
