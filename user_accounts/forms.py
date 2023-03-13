from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import EmailValidator

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django.forms import ModelForm, inlineformset_factory
from django.forms import BaseInlineFormSet
from django.forms import inlineformset_factory

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
