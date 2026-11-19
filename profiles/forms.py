
from django import forms
from .models import StudentProfile


class StudentProfileForm(forms.ModelForm):

    class Meta:
        model = StudentProfile

        fields = [
            'full_name',
            'phone',
            'location',
            'education',
            'skills',
            'resume',
            'profile_picture',
        ]

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),

            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your city'
            }),

            'education': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your qualification'
            }),

            'skills': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your skills',
                'rows': 4
            }),

            'profile_picture': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
