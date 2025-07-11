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

    path('frontend/', serve, {
        'document_root': os.path.join(BASE_DIR, 'static_frontend'),
        'path': 'index.html'
        }),
]
