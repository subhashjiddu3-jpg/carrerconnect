
from django import forms
from .models import Job, JobApplication, CompanyProfile


# 1. Job Form
class JobForm(forms.ModelForm):

    class Meta:
        model = Job

        fields = [
            'title',
            'company_name',
            'location',
            'job_type',
            'salary',
            'description',
            'requirements',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter job title'
            }),

            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company name'
            }),

            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter job location'
            }),

            'salary': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter salary'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),

            'requirements': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
        }


# 2. Job Application Form
class JobApplicationForm(forms.ModelForm):

    class Meta:
        model = JobApplication

        fields = [
            'resume',
            'cover_letter',
        ]

        widgets = {
            'resume': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),

            'cover_letter': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Why are you suitable for this job?'
            }),
        }


# 3. Company Profile Form
class CompanyProfileForm(forms.ModelForm):

    class Meta:
        model = CompanyProfile

        fields = [
            'company_name',
            'logo',
            'location',
            'description',
            'website',
        ]

        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company name'
            }),

            'logo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),

            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company location'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe your company'
            }),

            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.example.com'
            }),
        }
