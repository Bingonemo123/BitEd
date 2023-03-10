
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Profile
from .forms import CustomUserCreationForm, FormsetUserCreationForm
from django.views import generic
from django.urls import reverse_lazy
from tiles.models import WriteRequestData
from questions.models import Question
from user_accounts.forms import ActivateEmailMixin
from django.utils.encoding import force_str
from base64 import urlsafe_b64decode
from user_accounts.tokens import account_activation_token

# Create your views here.
class SignUpView(generic.CreateView, ActivateEmailMixin):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['formset'] = FormsetUserCreationForm(self.request.POST) 
        else:
            context['formset'] = FormsetUserCreationForm() 

        return context

    def form_valid(self, form):
        result = super().form_valid(form)
        self.send_activation_email(self.object, 
                                form.cleaned_data.get('email'))
       
        inlineformset = FormsetUserCreationForm(self.request.POST,
                                instance=self.object)

        if inlineformset.is_valid():
            inlineformset.save()
        else: 
            print(inlineformset.errors)
            print(inlineformset.non_form_errors())
        
        return result
    
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_b64decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
    
    return redirect('homepage')
    

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
