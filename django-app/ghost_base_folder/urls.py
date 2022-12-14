"""ghost_base_folder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from . import admin_url
from . import views
from . import settings


urlpatterns = [
    admin_url.path,
    path('tinymce/', include('tinymce.urls')),
    path('', views.HomeTemplateView.as_view(), name='home'),
    path('analytics/', include('analytics.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('transcribe/', include('transcribe.urls')),
    path('user/', include('user_management.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()
