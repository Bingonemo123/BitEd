from django.contrib.auth import get_user_model
from django.views import generic
from tiles.models import WriteRequestData
from questions.models import Question

# Create your views here.
class UserUpdateView(generic.UpdateView):
    model = get_user_model()    
    fields = ['username', 'first_name', 'last_name', 'email']

    def get_success_url(self):
        return self.request.path
    
class HistoryListView(generic.ListView):

    model = WriteRequestData

    def get_queryset(self):
        queryset =  super().get_queryset()
        return queryset.filter(requested_by=self.request.user)

class MyQuestionsListView(generic.ListView):
    model = Question

    def get_queryset(self):
        queryset =  super().get_queryset()
        return queryset.filter(owner=self.request.user)
