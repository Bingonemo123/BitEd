"""
bitedMainProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.views.generic import RedirectView
from home.views import dark_mode, google_auth
from .views import google_oauth_login

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='home')),
   # path('accounts/google/login/', google_auth, name='google_auth'),
   path('google-oauth-login/', google_oauth_login, name='google_oauth_login'),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('home/', include('home.urls')),
    path('registration/', include('registration.urls')),
    path('profile/', include('profile.urls')),
    path('writing/', include('writing.urls')),
    path('folder/', include('folder.urls')),
    path('question/', include('questions.urls')),
    path('verification/', include('verify_email.urls')),
    path('map/', include('map.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('dark_mode', dark_mode)
]
