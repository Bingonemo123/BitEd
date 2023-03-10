from django.urls import path
from .views import QuestionCreate
from .views import MyQuestionsUpdate
from .views import SelectTags

urlpatterns = [
    path('', QuestionCreate.as_view(), name="createQuestion"),
    path('question_update/<int:pk>', 
         MyQuestionsUpdate.as_view(), 
         name='question_update'),
    path('select_tags/<int:pk>',
         SelectTags.as_view(),
         name='select_tags')
]

