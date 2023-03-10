from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.validators import EmailValidator

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django.forms import ModelForm, inlineformset_factory
from django.forms import BaseInlineFormSet
from django.forms import inlineformset_factory

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage


from .tokens import account_activation_token
from .models import Profile

# info: https://www.youtube.com/watch?v=HdrOcreAXKk add extra registration fields
# multiple forms: https://stackoverflow.com/questions/12573992/multiple-forms-and-formsets-in-createview
# https://stackoverflow.com/questions/48388366/i-want-to-add-a-location-field-in-django-model-which-take-location-input-by-putt for location

def email_unique (value):
    if User.objects.filter(email=value).exists():
        raise ValidationError(
            _(f'{value} already Taken'),
            params={'value': value},
        )

class DateInput(forms.DateInput):
    input_type = 'date'

class ActivateEmailMixin:

    mail_subject = 'Activate your user account.'

    def send_activation_email(self, user, to_email):
        message = render_to_string('registration/activate_account.html', {
        'user': user.username,
        'domain': get_current_site(self.request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if self.request.is_secure() else 'http'
    })
        email = EmailMessage(self.mail_subject, message, to=[to_email])
        if email.send():
            messages.success(self.request, f'Dear {user}, please go to you email {to_email} inbox and click on \
                received activation link to confirm and complete the registration. Note: Check your spam folder.')
        else:
            messages.error(self.request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')

    def activate_email_msg(self, user, to_email):
        messages.success(self.request, f'Dear {user}, please go to you email {to_email} inbox and click on \
        received activation link to confirm and complete the registration. Note: Check your spam folder.')

class CustomUserCreationForm (UserCreationForm):
    error_css_class = 'login-customusercreationform-error'
    email = forms.EmailField(validators=[EmailValidator, email_unique])
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    def save(self, commit=True):
        self.instance.is_active = False
        return super().save(commit)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = ['birthday', 'location']
        widgets = {
            'birthday': DateInput(),
        }

class CustomProfileInlineFormSet(BaseInlineFormSet):

    def save(self, commit=True) :
        result =  super().save(commit=False)

        for SavingProfileModel in result:
            SavingProfileModel.id_user =  self.instance.id
        return super().save()


FormsetUserCreationForm = inlineformset_factory(User, Profile, form=ProfileForm,
                                                 can_delete=False, formset=CustomProfileInlineFormSet)
