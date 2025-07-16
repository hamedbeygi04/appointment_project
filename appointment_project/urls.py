"""
URL configuration for appointment_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from appointments.views import LogoutView

from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import os

BASE_DIR = settings.BASE_DIR

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('appointments.urls')),

    path('api/logout/', LogoutView.as_view(), name='logout'),

    path('', TemplateView.as_view(template_name="static_frontend/index.html"), name='index'),
    path('signup/', TemplateView.as_view(template_name='static_frontend/signup.html'), name='signup'),
    path('login/', TemplateView.as_view(template_name='static_frontend/login.html'), name='login'),
    path('appointment/', TemplateView.as_view(template_name='static_frontend/appointment.html'), name='appointment'),
    path('dashboard/', TemplateView.as_view(template_name='static_frontend/dashboard.html'), name='dashboard'),
    path('forgot-password/', TemplateView.as_view(template_name='static_frontend/forgot-password.html'), name='forgot-password'),
    path('reset-password/<uidb64>/<token>/', TemplateView.as_view(template_name='static_frontend/reset-password.html'), name='reset-password'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
