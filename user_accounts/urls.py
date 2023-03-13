from django.urls import path, include
from .views import SignUpView
from .views import UserAccountUpdateView
from .views import ProfileAccounUpdateView
from .views import HistoryListView
from .views import MyQuestionsListView

# for more details see: https://docs.djangoproject.com/en/4.1/topics/auth/default/#module-django.contrib.auth.views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls') ),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('user_update/<int:pk>/', UserAccountUpdateView.as_view(), name='user_update'),
    path('detail_update/<int:pk>/', ProfileAccounUpdateView.as_view(), name='detail_update' ),
    path('history/<int:pk>', HistoryListView.as_view(), name='history' ),
    path('my_questions/', MyQuestionsListView.as_view(), name='my_questions'),
]



