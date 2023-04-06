from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

# info: https://www.youtube.com/watch?v=HdrOcreAXKk add extra registration fields
# multiple forms: https://stackoverflow.com/questions/12573992/multiple-forms-and-formsets-in-createview
# https://stackoverflow.com/questions/48388366/i-want-to-add-a-location-field-in-django-model-which-take-location-input-by-putt for location

def email_unique (value):
    if get_user_model().objects.filter(email=value).exists():
        raise ValidationError(
            _(f'{value} already Taken'),
            params={'value': value},
        )

class CustomUserCreationForm (UserCreationForm):
    error_css_class = 'login-customusercreationform-error'
    email = forms.EmailField(validators=[EmailValidator, email_unique])
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    def save(self, commit=True):
        self.instance.is_active = False
        return super().save(commit)

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
