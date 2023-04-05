from django.urls import path, include
from writing.views import WritingView
from writing.views import ReviewingView
from writing.views import resume_wrd

app_name = 'writing'
urlpatterns = [
    path('answering/<int:pk>/', 
        WritingView.as_view(), 
        name='writing'),

    path('reviewing/<int:pk>/',
         ReviewingView.as_view(),
         name='reviewing'
         ),

    path('resume/<int:pk>/',
         resume_wrd,
         name='resume_block'
         )
]

