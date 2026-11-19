from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    path('jobs/', include('jobs.urls')),
    # Student accounts
    path('accounts/', include('accounts.urls')),

    # Login compatibility
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='accounts/login.html'
        ),
        name='login'
    ),

    # Homepage and profiles
    path('', include('profiles.urls')),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )