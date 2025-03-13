"""
URL configuration for khaochan_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from news.views import (
    home, login_view, newsletters_view, about_view, blog_view,
    publishers_view, help_view, terms_view, privacy_view, sitemap_view,
    signup_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('newsletters/', newsletters_view, name='newsletters'),
    path('about/', about_view, name='about'),
    path('blog/', blog_view, name='blog'),
    path('publishers/', publishers_view, name='publishers'),
    path('help/', help_view, name='help'),
    path('terms/', terms_view, name='terms'),
    path('privacy/', privacy_view, name='privacy'),
    path('sitemap/', sitemap_view, name='sitemap'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', signup_view, name='signup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
