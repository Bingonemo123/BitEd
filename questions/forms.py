from django import forms
from django.forms import ModelForm
from django.forms import formset_factory
from django.forms import modelformset_factory

from tiles.models import Tile
from questions.models import QuestionChoice


########## TILES ###########

class TileBooleanForm(ModelForm):
    is_selected = forms.BooleanField(required=False)

    def __init__(self, *args ,**kwargs):
        self.obj = kwargs.pop('obj')
        return super().__init__(*args, **kwargs)
    
    class Meta:
        model = Tile
        exclude = '__all__'

    def save(self, commit=True):
        self.instance.questions.add(self.obj)

SelectTilesFormset = modelformset_factory(Tile, 
                                         form = TileBooleanForm, 
                                         fields=[], 
                                         extra=0)


########### Question Creation ##############

class QuestionChoiceForm(ModelForm):

    class Meta:
        model = QuestionChoice
        fields = ['choice_text',]

basic_formset = formset_factory(QuestionChoiceForm, min_num=2,
                                        validate_min=True, extra=0)

class ChoiceFormset(basic_formset):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False
