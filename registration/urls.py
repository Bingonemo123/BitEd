from django.urls import path, include
from registration.views import SignUpView

# for more details see: https://docs.djangoproject.com/en/4.1/topics/auth/default/#module-django.contrib.auth.views

urlpatterns = [
    path('', include('django.contrib.auth.urls') ),
    path('signup/', SignUpView.as_view(), name='signup'),
]

