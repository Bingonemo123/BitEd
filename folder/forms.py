from django import forms
from django.forms import inlineformset_factory
from django.forms import formset_factory
from django.core.exceptions import ValidationError

from folder.models import BLOCK_MODE_CHOICES
from folder.models import BLOCK_SECTOR_CHOICES
from folder.models import Folder
from folder.rand import fastest_get_random_questions

class writeRequestDataForm(forms.Form):
    block_mode = forms.ChoiceField(choices=BLOCK_MODE_CHOICES, initial=2)
    block_total_questions = forms.IntegerField(initial=40)
    sector = forms.ChoiceField(choices=BLOCK_SECTOR_CHOICES)
    timed = forms.BooleanField(required=False)

    def __init__ (self, *args, **kwargs):
        self.questions_queryset = kwargs.pop('questions_queryset', None)
        super().__init__(*args, **kwargs)

    def clean_block_total_questions(self):  
        self.random_questions = fastest_get_random_questions(self.questions_queryset, 
                                   self.cleaned_data['block_total_questions'])
        if self.random_questions is None:
            raise ValidationError(f"""Not Enough Questions in Database.
                    Total Questions Found: {len(self.questions_queryset)} """, code='invalid')
        else:
            return self.cleaned_data['block_total_questions']
        
class SubfolderBooleanForm(forms.ModelForm):

    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_selected'] = forms.BooleanField(required=False,
                                                         label= str(self.instance))

    class Meta:
        model = Folder
        exclude = '__all__'
    
InlineSubfoldersListFormSet = inlineformset_factory(Folder, Folder,
                                                  form=SubfolderBooleanForm,
                                                  fields = [],
                                                  can_delete=False,
                                                  extra=0)



class PersonalQueryQuestionsForm(forms.Form):

    personal_filter_choices = (
        ['unseen', 'unseen'],
        ['mistakes', 'mistakes'],
        ['omitted', 'omitted'],
        ['correct', 'correct']
    )

    personal_filter = forms.MultipleChoiceField(choices=personal_filter_choices,
                                                widget=forms.CheckboxSelectMultiple,
                                                  required=False, 
                                                  label="Personal filter",
                                                  label_suffix="")

#### folder Create Form #####

class folderCreateForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name', 'type', 'parent']
