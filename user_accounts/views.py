
from django.contrib.auth.models import User
from .models import Profile
from .forms import CustomUserCreationForm
from django.views import generic
from django.urls import reverse_lazy
from tiles.models import WriteRequestData
from questions.models import Question
from django.contrib import messages
from verify_email.email_handler import send_verification_email

# Create your views here.
class SignUpView(generic.FormView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"

    def form_valid(self, form):
        inactive_user = send_verification_email(self.request, form)   
        messages.success(self.request, f'Dear {inactive_user}, \
                         please go to you email { form.cleaned_data.get("email")} inbox and click on \
                         received activation link to confirm \
                         and complete the registration. Note: Check your spam folder.')
        return super().form_valid(form)    

class UserAccountUpdateView(generic.UpdateView):
    model = User    
    fields = ['username', 'first_name', 'last_name', 'email']

    def get_success_url(self):
        return self.request.path
    
class ProfileAccounUpdateView(generic.UpdateView):
    model = Profile
    fields = ['birthday', 'bio', 'location']
    template_name = 'auth/detail_update.html'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = User._default_manager.all()
        user_obj = super().get_object(queryset)
        return user_obj.profile

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
