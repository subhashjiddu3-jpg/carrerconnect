
from io import BytesIO

from openpyxl import Workbook

from django.db import models
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail

from profiles.models import StudentProfile
from .forms import JobForm, JobApplicationForm, CompanyProfileForm
from .models import Job, JobApplication, CompanyProfile, Notification

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


# 1. Post a new job
@login_required
def post_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)

        if form.is_valid():
            job = form.save(commit=False)
            job.company = request.user
            job.save()
            return redirect('post_job')
    else:
        form = JobForm()

    return render(request, 'jobs/post_job.html', {'form': form})


# 2. Display jobs with search and filters
def job_list(request):
    jobs = Job.objects.filter(
        is_active=True
    ).order_by('-created_at')

    search_query = request.GET.get('search', '').strip()
    location = request.GET.get('location', '').strip()
    job_type = request.GET.get('job_type', '').strip()

    if search_query:
        jobs = jobs.filter(title__icontains=search_query)

    if location:
        jobs = jobs.filter(location__icontains=location)

    if job_type:
        jobs = jobs.filter(job_type__icontains=job_type)

    return render(request, 'jobs/job_list.html', {
        'jobs': jobs,
        'search_query': search_query,
        'location': location,
        'selected_job_type': job_type,
    })


# 3. Job details
def job_detail(request, job_id):
    job = get_object_or_404(
        Job,
        id=job_id,
        is_active=True
    )

    return render(
        request,
        'jobs/job_detail.html',
        {'job': job}
    )


# 4. Apply for a job
@login_required
def apply_job(request, job_id):
    job = get_object_or_404(
        Job,
        id=job_id,
        is_active=True
    )

    if request.method == 'POST':
        form = JobApplicationForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.student = request.user
            application.save()
            return redirect('my_applications')
    else:
        form = JobApplicationForm()

    return render(request, 'jobs/apply_job.html', {
        'form': form,
        'job': job
    })


# 5. My applications
@login_required
def my_applications(request):
    applications = JobApplication.objects.filter(
        student=request.user
    ).order_by('-id')

    return render(request, 'jobs/my_applications.html', {
        'applications': applications,
        'total_applications': applications.count(),
        'pending_applications': applications.filter(
            status='Pending'
        ).count(),
        'shortlisted_applications': applications.filter(
            status='Shortlisted'
        ).count(),
        'rejected_applications': applications.filter(
            status='Rejected'
        ).count(),
        'selected_applications': applications.filter(
            status='Selected'
        ).count(),
    })


# 6. Company applications
@login_required
def company_applications(request):
    if not CompanyProfile.objects.filter(
        company=request.user
    ).exists():
        return redirect('company_profile')

    applications = JobApplication.objects.filter(
        job__company=request.user
    ).select_related(
        'job',
        'student'
    ).order_by('-applied_at')

    return render(
        request,
        'jobs/company_applications.html',
        {'applications': applications}
    )


# 7. Company dashboard
@login_required
def company_dashboard(request):
    if not CompanyProfile.objects.filter(
        company=request.user
    ).exists():
        return redirect('company_profile')

    jobs = Job.objects.filter(
        company=request.user
    ).order_by('-created_at')

    applications = JobApplication.objects.filter(
        job__company=request.user
    )

    context = {
        'total_jobs': jobs.count(),
        'active_jobs': jobs.filter(is_active=True).count(),
        'total_applications': applications.count(),
        'pending_applications': applications.filter(
            status='Pending'
        ).count(),
        'shortlisted_applications': applications.filter(
            status='Shortlisted'
        ).count(),
        'selected_applications': applications.filter(
            status='Selected'
        ).count(),
        'rejected_applications': applications.filter(
            status='Rejected'
        ).count(),
        'recent_jobs': jobs[:5],
        'recent_applications': applications.order_by(
            '-applied_at'
        )[:5],
    }

    return render(
        request,
        'jobs/company_dashboard.html',
        context
    )


# 8. Update application status and notify student
@login_required
def update_application_status(request, application_id):
    if request.method != 'POST':
        return redirect('company_applications')

    application = get_object_or_404(
        JobApplication,
        id=application_id,
        job__company=request.user
    )

    new_status = request.POST.get('status')

    allowed_statuses = [
        'Pending',
        'Shortlisted',
        'Rejected',
        'Selected'
    ]

    if new_status in allowed_statuses:
        old_status = application.status

        if new_status != old_status:
            application.status = new_status
            application.save()

            Notification.objects.create(
                student=application.student,
                application=application,
                message=(
                    f"Your application for "
                    f"{application.job.title} "
                    f"has been updated to {new_status}."
                )
            )

            if application.student.email:
                subject = 'CareerConnect - Application Status Update'

                message = (
                    f"Hello {application.student.username},\n\n"
                    f"Your application status has been updated.\n\n"
                    f"Job: {application.job.title}\n"
                    f"Company: {application.job.company_name}\n"
                    f"New Status: {new_status}\n\n"
                    f"Thank you for using CareerConnect."
                )

                send_mail(
                    subject,
                    message,
                    None,
                    [application.student.email],
                    fail_silently=False
                )

    return redirect('company_applications')


# 9. Create or edit company profile
@login_required
def company_profile(request):
    profile = CompanyProfile.objects.filter(
        company=request.user
    ).first()

    if request.method == 'POST':
        form = CompanyProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            company = form.save(commit=False)
            company.company = request.user
            company.save()
            return redirect('company_profile')
    else:
        form = CompanyProfileForm(instance=profile)

    return render(request, 'jobs/company_profile.html', {
        'form': form,
        'profile': profile
    })


# 10. Public company profile
def company_profile_detail(request, company_id):
    profile = get_object_or_404(
        CompanyProfile,
        id=company_id
    )

    company_jobs = Job.objects.filter(
        company=profile.company,
        is_active=True
    ).order_by('-created_at')

    return render(
        request,
        'jobs/company_profile_detail.html',
        {
            'profile': profile,
            'company_jobs': company_jobs,
        }
    )


# 11. Student notifications
@login_required
def student_notifications(request):
    notifications = Notification.objects.filter(
        student=request.user
    ).order_by('-created_at')

    unread_count = notifications.filter(
        is_read=False
    ).count()

    return render(request, 'jobs/student_notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })


# 12. Mark one notification as read
@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(
        Notification,
        id=notification_id,
        student=request.user
    )

    if request.method == 'POST':
        notification.is_read = True
        notification.save()

    return redirect('student_notifications')


# 13. Mark all notifications as read
@login_required
def mark_all_notifications_read(request):
    if request.method == 'POST':
        Notification.objects.filter(
            student=request.user,
            is_read=False
        ).update(is_read=True)

    return redirect('student_notifications')


# 14. Delete notification
@login_required
def delete_notification(request, notification_id):
    notification = get_object_or_404(
        Notification,
        id=notification_id,
        student=request.user
    )

    if request.method == 'POST':
        notification.delete()

    return redirect('student_notifications')


# 15. Edit job - only the owner
@login_required
def edit_job(request, job_id):
    job = get_object_or_404(
        Job,
        id=job_id,
        company=request.user
    )

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)

        if form.is_valid():
            form.save()
            return redirect('company_dashboard')
    else:
        form = JobForm(instance=job)

    return render(request, 'jobs/edit_job.html', {
        'form': form,
        'job': job
    })


# 16. Delete job - only the owner
@login_required
def delete_job(request, job_id):
    job = get_object_or_404(
        Job,
        id=job_id,
        company=request.user
    )

    if request.method == 'POST':
        job.delete()
        return redirect('company_dashboard')

    return render(
        request,
        'jobs/delete_job.html',
        {'job': job}
    )


# 17. Student dashboard
@login_required
def student_dashboard(request):
    applications = JobApplication.objects.filter(
        student=request.user
    ).order_by('-applied_at')

    total_applications = applications.count()

    pending_applications = applications.filter(
        status='Pending'
    ).count()

    shortlisted_applications = applications.filter(
        status='Shortlisted'
    ).count()

    selected_applications = applications.filter(
        status='Selected'
    ).count()

    rejected_applications = applications.filter(
        status='Rejected'
    ).count()

    recent_applications = applications[:5]

    student_profile = StudentProfile.objects.filter(
        user=request.user
    ).first()

    required_fields = [
        ('Full Name', student_profile.full_name if student_profile else ''),
        ('Phone Number', student_profile.phone if student_profile else ''),
        ('Location', student_profile.location if student_profile else ''),
        ('Education', student_profile.education if student_profile else ''),
        ('Skills', student_profile.skills if student_profile else ''),
    ]

    completed_fields = 0
    missing_fields = []

    for field_name, field_value in required_fields:
        if field_value and field_value.strip():
            completed_fields += 1
        else:
            missing_fields.append(field_name)

    profile_completion = int(
        (completed_fields / len(required_fields)) * 100
    )

    notifications = Notification.objects.filter(
        student=request.user
    ).order_by('-created_at')[:5]

    available_jobs = Job.objects.filter(
        is_active=True
    ).order_by('-created_at')[:5]

    return render(request, 'jobs/student_dashboard.html', {
        'total_applications': total_applications,
        'pending_applications': pending_applications,
        'shortlisted_applications': shortlisted_applications,
        'selected_applications': selected_applications,
        'rejected_applications': rejected_applications,
        'recent_applications': recent_applications,
        'student_profile': student_profile,
        'profile_completion': profile_completion,
        'missing_fields': missing_fields,
        'notifications': notifications,
        'available_jobs': available_jobs,
    })


# 18. Admin analytics dashboard
@staff_member_required
def admin_analytics(request):
    total_students = StudentProfile.objects.count()
    total_companies = CompanyProfile.objects.count()

    recent_students = StudentProfile.objects.order_by(
        '-created_at'
    )[:5]

    education_stats = (
        StudentProfile.objects
        .values('education')
        .annotate(total=models.Count('id'))
        .order_by('-total')
    )

    location_stats = (
        StudentProfile.objects
        .values('location')
        .annotate(total=models.Count('id'))
        .order_by('-total')
    )

    total_jobs = Job.objects.count()
    active_jobs = Job.objects.filter(is_active=True).count()
    inactive_jobs = Job.objects.filter(is_active=False).count()

    full_time_jobs = Job.objects.filter(
        job_type='Full Time'
    ).count()

    part_time_jobs = Job.objects.filter(
        job_type='Part Time'
    ).count()

    internship_jobs = Job.objects.filter(
        job_type='Internship'
    ).count()

    remote_jobs = Job.objects.filter(
        job_type='Remote'
    ).count()

    total_applications = JobApplication.objects.count()

    selected_applications = JobApplication.objects.filter(
        status='Selected'
    ).count()

    pending_applications = JobApplication.objects.filter(
        status='Pending'
    ).count()

    shortlisted_applications = JobApplication.objects.filter(
        status='Shortlisted'
    ).count()

    rejected_applications = JobApplication.objects.filter(
        status='Rejected'
    ).count()

    monthly_student_registrations = (
        StudentProfile.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=models.Count('id'))
        .order_by('month')
    )

    monthly_job_applications = (
        JobApplication.objects
        .annotate(month=TruncMonth('applied_at'))
        .values('month')
        .annotate(total=models.Count('id'))
        .order_by('month')
    )

    student_monthly_data = list(monthly_student_registrations)
    application_monthly_data = list(monthly_job_applications)

    max_student_count = max(
        [item['total'] for item in student_monthly_data],
        default=1
    )

    max_application_count = max(
        [item['total'] for item in application_monthly_data],
        default=1
    )

    for item in student_monthly_data:
        item['month_label'] = item['month'].strftime('%B %Y')
        item['percentage'] = (
            item['total'] / max_student_count
        ) * 100

    for item in application_monthly_data:
        item['month_label'] = item['month'].strftime('%B %Y')
        item['percentage'] = (
            item['total'] / max_application_count
        ) * 100

    context = {
        'total_students': total_students,
        'total_companies': total_companies,
        'recent_students': recent_students,
        'education_stats': education_stats,
        'location_stats': location_stats,
        'total_jobs': total_jobs,
        'active_jobs': active_jobs,
        'inactive_jobs': inactive_jobs,
        'full_time_jobs': full_time_jobs,
        'part_time_jobs': part_time_jobs,
        'internship_jobs': internship_jobs,
        'remote_jobs': remote_jobs,
        'total_applications': total_applications,
        'selected_applications': selected_applications,
        'pending_applications': pending_applications,
        'shortlisted_applications': shortlisted_applications,
        'rejected_applications': rejected_applications,
        'monthly_student_registrations': student_monthly_data,
        'monthly_job_applications': application_monthly_data,
    }

    return render(
        request,
        'jobs/admin_analytics.html',
        context
    )


# 19. Download admin analytics as PDF
@staff_member_required
def download_analytics_pdf(request):
    buffer = BytesIO()

    pdf = SimpleDocTemplate(
        buffer,
        pagesize=A4
    )

    styles = getSampleStyleSheet()
    elements = []

    elements.append(
        Paragraph(
            "CareerConnect - Admin Analytics Report",
            styles['Title']
        )
    )

    elements.append(Spacer(1, 20))

    data = [
        ['Analytics', 'Total'],
        ['Total Students', StudentProfile.objects.count()],
        ['Total Companies', CompanyProfile.objects.count()],
        ['Total Jobs', Job.objects.count()],
        ['Total Applications', JobApplication.objects.count()],
        [
            'Selected Applications',
            JobApplication.objects.filter(status='Selected').count()
        ],
        [
            'Pending Applications',
            JobApplication.objects.filter(status='Pending').count()
        ],
        [
            'Shortlisted Applications',
            JobApplication.objects.filter(status='Shortlisted').count()
        ],
        [
            'Rejected Applications',
            JobApplication.objects.filter(status='Rejected').count()
        ],
    ]

    table = Table(data, colWidths=[280, 150])

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))

    elements.append(table)
    pdf.build(elements)
    buffer.seek(0)

    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        'attachment; filename="CareerConnect_Analytics.pdf"'
    )

    return response


# 20. Download admin analytics as Excel
@staff_member_required
def download_analytics_excel(request):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "CareerConnect Analytics"

    sheet.append(["CareerConnect - Admin Analytics Report"])
    sheet.append([])
    sheet.append(["Analytics", "Total"])

    sheet.append(["Total Students", StudentProfile.objects.count()])
    sheet.append(["Total Companies", CompanyProfile.objects.count()])
    sheet.append(["Total Jobs", Job.objects.count()])
    sheet.append(["Total Applications", JobApplication.objects.count()])

    sheet.append([
        "Selected Applications",
        JobApplication.objects.filter(status="Selected").count()
    ])

    sheet.append([
        "Pending Applications",
        JobApplication.objects.filter(status="Pending").count()
    ])

    sheet.append([
        "Shortlisted Applications",
        JobApplication.objects.filter(status="Shortlisted").count()
    ])

    sheet.append([
        "Rejected Applications",
        JobApplication.objects.filter(status="Rejected").count()
    ])

    sheet.column_dimensions["A"].width = 30
    sheet.column_dimensions["B"].width = 20

    response = HttpResponse(
        content_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
    )

    response["Content-Disposition"] = (
        'attachment; filename="CareerConnect_Analytics.xlsx"'
    )

    workbook.save(response)
    return response


# 21. Company analytics dashboard
@login_required
def company_analytics(request):
    if not CompanyProfile.objects.filter(
        company=request.user
    ).exists():
        return redirect('company_profile')

    company_jobs = Job.objects.filter(
        company=request.user
    )

    applications = JobApplication.objects.filter(
        job__company=request.user
    )

    context = {
        'total_jobs': company_jobs.count(),
        'total_applications': applications.count(),
        'selected_applications': applications.filter(
            status='Selected'
        ).count(),
        'pending_applications': applications.filter(
            status='Pending'
        ).count(),
        'shortlisted_applications': applications.filter(
            status='Shortlisted'
        ).count(),
        'rejected_applications': applications.filter(
            status='Rejected'
        ).count(),
    }

    return render(
        request,
        'jobs/company_analytics.html',
        context
    )


# 22. Company performance report
@login_required
def company_performance(request):
    if not CompanyProfile.objects.filter(
        company=request.user
    ).exists():
        return redirect('company_profile')

    company_jobs = Job.objects.filter(
        company=request.user
    )

    monthly_jobs = (
        company_jobs
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=models.Count('id'))
        .order_by('month')
    )

    monthly_applications = (
        JobApplication.objects
        .filter(job__company=request.user)
        .annotate(month=TruncMonth('applied_at'))
        .values('month')
        .annotate(total=models.Count('id'))
        .order_by('month')
    )

    context = {
        'monthly_jobs': [
            {
                'month': item['month'].strftime('%B %Y'),
                'total': item['total']
            }
            for item in monthly_jobs
        ],
        'monthly_applications': [
            {
                'month': item['month'].strftime('%B %Y'),
                'total': item['total']
            }
            for item in monthly_applications
        ],
    }

    return render(
        request,
        'jobs/company_performance.html',
        context
    )


# 23. Download company performance report as PDF
@login_required
def download_company_performance_pdf(request):
    if not CompanyProfile.objects.filter(
        company=request.user
    ).exists():
        return redirect('company_profile')

    buffer = BytesIO()

    pdf = SimpleDocTemplate(
        buffer,
        pagesize=A4
    )

    styles = getSampleStyleSheet()
    elements = []

    elements.append(
        Paragraph(
            "CareerConnect - Company Performance Report",
            styles['Title']
        )
    )

    elements.append(Spacer(1, 20))

    company_jobs = Job.objects.filter(
        company=request.user
    )

    applications = JobApplication.objects.filter(
        job__company=request.user
    )

    data = [
        ['Analytics', 'Total'],
        ['Company Username', request.user.username],
        ['Total Jobs Posted', company_jobs.count()],
        ['Total Applications', applications.count()],
        [
            'Selected Candidates',
            applications.filter(status='Selected').count()
        ],
        [
            'Pending Applications',
            applications.filter(status='Pending').count()
        ],
        [
            'Shortlisted Candidates',
            applications.filter(status='Shortlisted').count()
        ],
        [
            'Rejected Applications',
            applications.filter(status='Rejected').count()
        ],
    ]

    table = Table(data, colWidths=[280, 150])

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))

    elements.append(table)
    pdf.build(elements)
    buffer.seek(0)

    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        'attachment; filename="Company_Performance_Report.pdf"'
    )

    return response


# 24. Download company performance report as Excel
@login_required
def download_company_performance_excel(request):
    if not CompanyProfile.objects.filter(
        company=request.user
    ).exists():
        return redirect('company_profile')

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Company Performance"

    company_jobs = Job.objects.filter(
        company=request.user
    )

    applications = JobApplication.objects.filter(
        job__company=request.user
    )

    sheet.append(["CareerConnect - Company Performance Report"])
    sheet.append([])
    sheet.append(["Analytics", "Total"])

    sheet.append(["Company Username", request.user.username])
    sheet.append(["Total Jobs Posted", company_jobs.count()])
    sheet.append(["Total Applications", applications.count()])

    sheet.append([
        "Selected Candidates",
        applications.filter(status="Selected").count()
    ])

    sheet.append([
        "Pending Applications",
        applications.filter(status="Pending").count()
    ])

    sheet.append([
        "Shortlisted Candidates",
        applications.filter(status="Shortlisted").count()
    ])

    sheet.append([
        "Rejected Applications",
        applications.filter(status="Rejected").count()
    ])

    sheet.column_dimensions["A"].width = 30
    sheet.column_dimensions["B"].width = 20

    response = HttpResponse(
        content_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
    )

    response["Content-Disposition"] = (
        'attachment; filename="Company_Performance_Report.xlsx"'
    )

    workbook.save(response)
    return response
