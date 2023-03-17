from django.urls import path

from tiles import views

app_name = 'tiles'
urlpatterns = [
    path('<int:pk>/', views.TileView.as_view(), name='tile_detail_view'),
    path('create/', views.TileCreateView.as_view(), name='tile_create_view')
]

