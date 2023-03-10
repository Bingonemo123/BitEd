from django.urls import path
from .views import load_home_page

urlpatterns = [
    path('', load_home_page, name="load_home_page"),
]

