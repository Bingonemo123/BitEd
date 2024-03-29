from django import forms
from django.forms import ModelForm
from django.forms import formset_factory
from django.forms import modelformset_factory

from folder.models import Folder
from questions.models import QuestionChoice
from questions.models import Question

########## CREATE #########

class QuestionCreateForm(ModelForm):
    class Meta:
        model = Question
 
        fields = ['question_title', 
                'question_body', 
                'question_explanation', 
                'tags']
        
        widgets ={
            'tags': forms.TextInput(attrs={"data-role":"tagsinput",
                                    "class":"form-control"})
        }

########### Question Creation ##############

class QuestionChoiceForm(ModelForm):

    class Meta:
        model = QuestionChoice
        fields = ['choice_text',]
        widgets = {
            'choice_text': forms.Textarea(attrs={'rows': 1})
        }

basic_formset = formset_factory(QuestionChoiceForm, min_num=2,
                                        validate_min=True, extra=0)

class ChoiceFormset(basic_formset):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

########## Folders ###########

class FolderSelectionForm(forms.ModelForm):

    # class Meta:
    #     model = Question
    #     fields = []

    folders = forms.ModelMultipleChoiceField(
        queryset=Folder.objects.all()
    )
    class Meta:
        model = Question
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Here we fetch the currently related projects into the field,     
        # so that they will display in the form.
        if self.instance.id:
            self.fields['folders'].initial = self.instance.folder_set.all(
            ).values_list('id', flat=True)

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)

        # Here we save the modified project selection back into the database
        instance.folder_set.set(self.cleaned_data['folders'])

        return instance
