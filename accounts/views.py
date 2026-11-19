
from profiles.models import StudentProfile
from jobs.models import Job, JobApplication, Notification

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


# Home Page
def home(request):
    return render(request, 'home.html')


# Student Registration
def register(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


# Student Dashboard
@login_required
def dashboard(request):

    # Recommended Jobs
    recommended_jobs = Job.objects.filter(
        is_active=True
    ).order_by('-created_at')[:5]

    # Student Application Statistics
    applications = JobApplication.objects.filter(
        student=request.user
    )

    total_applications = applications.count()

    pending_applications = applications.filter(
        status='Pending'
    ).count()

    shortlisted_applications = applications.filter(
        status='Shortlisted'
    ).count()

    rejected_applications = applications.filter(
        status='Rejected'
    ).count()

    selected_applications = applications.filter(
        status='Selected'
    ).count()

    # Unread Notifications Count
    unread_notifications_count = Notification.objects.filter(
        student=request.user,
        is_read=False
    ).count()

    # Dashboard Data
    return render(request, 'accounts/dashboard.html', {

        'recommended_jobs': recommended_jobs,

        'total_applications': total_applications,

        'pending_applications': pending_applications,

        'shortlisted_applications': shortlisted_applications,

        'rejected_applications': rejected_applications,

        'selected_applications': selected_applications,

        'unread_notifications_count': unread_notifications_count,

    })