from django.views.generic import FormView
from django.contrib import messages
from django.urls import reverse_lazy
from registration.forms import CustomUserCreationForm

from verify_email.email_handler import send_verification_email

# Create your views here.

class SignUpView(FormView):
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
