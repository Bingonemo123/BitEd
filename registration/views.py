from django.views.generic import RedirectView
from django.urls import reverse_lazy
from registration.forms import CustomUserCreationForm


# Create your views here.

class SignUpView(RedirectView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"

    def form_valid(self, form):
        return super().form_valid(form)
