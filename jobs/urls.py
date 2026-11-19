
from django.urls import path
from . import views

urlpatterns = [

    # Job URLs
    path('', views.job_list, name='job_list'),
    path('post/', views.post_job, name='post_job'),

    # Notification URLs
    path('notifications/', views.student_notifications, name='student_notifications'),
    path('notifications/read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/read-all/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    path('notifications/delete/<int:notification_id>/', views.delete_notification, name='delete_notification'),

    # Application URLs
    path('my-applications/', views.my_applications, name='my_applications'),
    path('company-applications/', views.company_applications, name='company_applications'),
    path('update-status/<int:application_id>/', views.update_application_status, name='update_application_status'),

    # Company URLs
    path('company-profile/', views.company_profile, name='company_profile'),
    path('company/<int:company_id>/', views.company_profile_detail, name='company_profile_detail'),
    path('company-dashboard/', views.company_dashboard, name='company_dashboard'),
    path('company-analytics/', views.company_analytics, name='company_analytics'),
    path('company-performance/', views.company_performance, name='company_performance'),
    path('company-performance/download-pdf/', views.download_company_performance_pdf, name='download_company_performance_pdf'),
    path('company-performance/download-excel/', views.download_company_performance_excel, name='download_company_performance_excel'),

    # Job Management
    path('edit-job/<int:job_id>/', views.edit_job, name='edit_job'),
    path('delete-job/<int:job_id>/', views.delete_job, name='delete_job'),

    # Student Dashboard
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),

    # Admin Analytics
    path('admin-analytics/', views.admin_analytics, name='admin_analytics'),
    path('admin-analytics/download-pdf/', views.download_analytics_pdf, name='download_analytics_pdf'),
    path('admin-analytics/download-excel/', views.download_analytics_excel, name='download_analytics_excel'),

    # Job Detail and Apply URLs - keep at the bottom
    path('<int:job_id>/', views.job_detail, name='job_detail'),
    path('<int:job_id>/apply/', views.apply_job, name='apply_job'),
]