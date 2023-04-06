from django.urls import path, include
from profile.views import UserUpdateView
from profile.views import HistoryListView
from profile.views import MyQuestionsListView

# for more details see: https://docs.djangoproject.com/en/4.1/topics/auth/default/#module-django.contrib.auth.views

urlpatterns = [
    path('user_update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('history/<int:pk>', HistoryListView.as_view(), name='history' ),
    path('my_questions/', MyQuestionsListView.as_view(), name='my_questions'),
]



