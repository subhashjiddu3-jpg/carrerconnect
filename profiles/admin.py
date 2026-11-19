from django.contrib import admin
from .models import StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'full_name',
        'phone',
        'location',
        'education',
    )

    search_fields = (
        'full_name',
        'phone',
        'location',
        'user__username',
    )

    list_filter = (
        'location',
        'education',
    )

    ordering = ('full_name',)