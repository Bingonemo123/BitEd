from django.urls import path

from folder import views

app_name = 'folder'
urlpatterns = [
    path('<int:pk>/', views.folderView.as_view(), name='folder_detail_view'),
    path('create/', views.folderCreateView.as_view(), name='folder_create_view'),
    path('my_folders/', views.MyfoldersListView.as_view(), name='folder_list_view')
]

