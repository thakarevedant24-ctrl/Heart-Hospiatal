from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control rounded-3',
                'placeholder': 'Enter your full name',
                'required': 'required',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control rounded-3',
                'placeholder': 'name@example.com',
                'required': 'required',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control rounded-3',
                'placeholder': '+91XXXXXXXX50',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control rounded-3',
                'placeholder': 'Subject of your inquiry',
                'required': 'required',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control rounded-3',
                'placeholder': 'Please detail your medical inquiry, question, or feedback...',
                'rows': 5,
                'required': 'required',
            }),
        }
