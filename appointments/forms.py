import datetime
from django import forms
from .models import Appointment
from departments.models import Department
from doctors.models import Doctor

TIME_SLOT_CHOICES = [
    ('', '-- Select Preferred Time --'),
    ('09:00:00', '09:00 AM'),
    ('09:30:00', '09:30 AM'),
    ('10:00:00', '10:00 AM'),
    ('10:30:00', '10:30 AM'),
    ('11:00:00', '11:00 AM'),
    ('11:30:00', '11:30 AM'),
    ('12:00:00', '12:00 PM'),
    ('12:30:00', '12:30 PM'),
    ('13:00:00', '01:00 PM'),
    ('13:30:00', '01:30 PM'),
    ('14:00:00', '02:00 PM'),
    ('14:30:00', '02:30 PM'),
    ('15:00:00', '03:00 PM'),
    ('15:30:00', '03:30 PM'),
    ('16:00:00', '04:00 PM'),
    ('16:30:00', '04:30 PM'),
    ('17:00:00', '05:00 PM'),
]

class AppointmentForm(forms.ModelForm):
    preferred_time = forms.ChoiceField(
        choices=TIME_SLOT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select rounded-3',
            'required': 'required',
        })
    )

    class Meta:
        model = Appointment
        fields = [
            'patient_name',
            'email',
            'phone',
            'department',
            'doctor',
            'preferred_date',
            'preferred_time',
            'notes',
        ]
        widgets = {
            'patient_name': forms.TextInput(attrs={
                'class': 'form-control rounded-3',
                'placeholder': 'Enter your full name',
                'required': 'required',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control rounded-3',
                'placeholder': 'patient@example.com',
                'required': 'required',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control rounded-3',
                'placeholder': '+1 (555) 000-0000',
                'required': 'required',
            }),
            'department': forms.Select(attrs={
                'class': 'form-select rounded-3',
                'id': 'id_department',
                'required': 'required',
            }),
            'doctor': forms.Select(attrs={
                'class': 'form-select rounded-3',
                'id': 'id_doctor',
            }),
            'preferred_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control rounded-3',
                'required': 'required',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control rounded-3',
                'placeholder': 'Briefly describe your symptoms, reason for consultation, or special requirements...',
                'rows': 3,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].queryset = Department.objects.all().order_by('name')
        self.fields['department'].empty_label = '-- Select Clinical Department --'
        self.fields['doctor'].queryset = Doctor.objects.filter(is_active=True).order_by('name')
        self.fields['doctor'].empty_label = '-- Any Available Specialist --'
        self.fields['doctor'].required = False

        # Set minimum date attribute dynamically on the widget
        today = datetime.date.today().isoformat()
        self.fields['preferred_date'].widget.attrs['min'] = today

    def clean_preferred_date(self):
        preferred_date = self.cleaned_data.get('preferred_date')
        if preferred_date and preferred_date < datetime.date.today():
            raise forms.ValidationError("Preferred appointment date cannot be in the past.")
        return preferred_date

    def clean(self):
        cleaned_data = super().clean()
        department = cleaned_data.get('department')
        doctor = cleaned_data.get('doctor')

        if doctor and department and doctor.department != department:
            self.add_error(
                'doctor',
                f"Dr. {doctor.name} is in the {doctor.department.name} department, not {department.name}."
            )

        return cleaned_data
