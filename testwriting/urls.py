from django.urls import path, include
from .views import WritingView
from .views import ReviewView

app_name = 'testwriting'

urlpatterns = [
    path('tw'+'/<int:pk>/', 
        WritingView.as_view(), 
        name='testWriting_view'),
    path('rev/<int:pk>/',
         ReviewView.as_view(),
         name='review'
         )
]

