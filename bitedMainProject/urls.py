"""bitedMainProject URL Configuration

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



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home_page.urls')), # TODO: Rendame home_page app to home
    path('', include('user_accounts.urls')), # TODO: Separate user_accounts in registration and profile
    path('', include('testwriting.urls')),
    path('tiles/', include('tiles.urls')),
    path('create/', include('questions.urls')),
    path('verification/', include('verify_email.urls'))
]
