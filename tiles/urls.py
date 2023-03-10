from django.urls import path

from . import views
from django.views.generic import TemplateView

app_name = 'tiles'
urlpatterns = [
    path('<int:pk>/', views.TileView.as_view(), name='tile_detail_view')
]

