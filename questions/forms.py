from django.core.exceptions import ValidationError
from django.forms import BaseFormSet
from django.forms import modelformset_factory
from django.forms import BaseModelForm
from django.forms import ModelForm
from django import forms

from tiles.models import HomePageTile
from questions.models import Question

class BaseChoiceFormset(BaseFormSet):

    def clean(self) -> None:
        return super().clean()

########## TAGS ###########

class TileBooleanForm(ModelForm):
    is_selected = forms.BooleanField(required=False)

    def __init__(self, *args ,**kwargs):
        self.obj = kwargs.pop('obj')
        return super().__init__(*args, **kwargs)
    
    class Meta:
        model = HomePageTile
        exclude = '__all__'

    def save(self, commit=True):
        self.instance.questions.add(self.obj)

SelectTagsFormset = modelformset_factory(HomePageTile, 
                                         form = TileBooleanForm, 
                                         fields=[], 
                                         extra=0)
