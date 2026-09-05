from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=120)
    photo = models.ImageField(upload_to='doctors/', blank=True, null=True)
    department = models.ForeignKey(
        'departments.Department',
        on_delete=models.CASCADE,
        related_name='doctors'
    )
    specialization = models.CharField(max_length=150)
    qualification = models.CharField(max_length=150)
    experience_years = models.PositiveIntegerField(default=1)
    bio = models.TextField()
    available_days = models.CharField(
        max_length=100, 
        default="Mon-Fri", 
        help_text='e.g. "Mon-Fri" or "Mon, Wed, Fri"'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'

    def __str__(self):
        return f"Dr. {self.name} ({self.specialization})"
