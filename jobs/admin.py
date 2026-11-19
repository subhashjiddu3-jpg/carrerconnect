
from django.contrib import admin
from .models import Job, JobApplication, CompanyProfile, Notification


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'company_name',
        'location',
        'job_type',
        'salary',
        'is_active',
        'created_at',
    )

    list_filter = (
        'job_type',
        'is_active',
        'created_at',
    )

    search_fields = (
        'title',
        'company_name',
        'location',
    )

    list_editable = ('is_active',)

    ordering = ('-created_at',)


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):

    list_display = (
        'student',
        'job',
        'status',
        'applied_at',
    )

    list_filter = (
        'status',
        'applied_at',
    )

    search_fields = (
        'student__username',
        'job__title',
    )


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'company_name',
        'company',
        'location',
    )

    search_fields = (
        'company_name',
        'location',
    )
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = (
        'student',
        'application',
        'message',
        'is_read',
        'created_at',
    )

    list_filter = (
        'is_read',
        'created_at',
    )

    search_fields = (
        'student__username',
        'message',
    )

    list_editable = ('is_read',)

    ordering = ('-created_at',)