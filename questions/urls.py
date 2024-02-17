from django.urls import path
from questions.views import QuestionCreate
from questions.views import MyQuestionsUpdate
from questions.views import SelectFolders
from questions.views import QuestionPreview

urlpatterns = [
     path('',
          QuestionCreate.as_view(),
          name="createQuestion"),
     path('update/<int:pk>',
          MyQuestionsUpdate.as_view(),
          name='question_update'),
     path('select_folders/<int:pk>',
          SelectFolders.as_view(),
          name='select_folders'),
     path('preview/<int:pk>',
          QuestionPreview.as_view(),
          name='review')
]
