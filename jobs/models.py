
from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):

    JOB_TYPES = [
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Internship', 'Internship'),
        ('Remote', 'Remote'),
    ]

    company = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posted_jobs'
    )

    title = models.CharField(max_length=200)

    company_name = models.CharField(max_length=200)

    location = models.CharField(max_length=200)

    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPES,
        default='Full Time'
    )

    salary = models.CharField(max_length=100)

    description = models.TextField()

    requirements = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class JobApplication(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shortlisted', 'Shortlisted'),
        ('Rejected', 'Rejected'),
        ('Selected', 'Selected'),
    ]

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='job_applications'
    )

    resume = models.FileField(
        upload_to='applications/resumes/',
        blank=True,
        null=True
    )

    cover_letter = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.student.username} - {self.job.title}"

# Company Profile Model
class CompanyProfile(models.Model):

    company = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='company_profile'
    )

    company_name = models.CharField(max_length=200)

    logo = models.ImageField(
        upload_to='company_logos/',
        blank=True,
        null=True
    )

    location = models.CharField(max_length=200)

    description = models.TextField()

    website = models.URLField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.company_name

# Application Notification Model

class Notification(models.Model):

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    application = models.ForeignKey(
        JobApplication,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    message = models.CharField(max_length=255)

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
