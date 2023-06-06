from django import forms

from writing.models import QuestionChoice
from writing.models import UserAnswer

# Forms
# https://stackoverflow.com/questions/27321692/override-a-django-generic-class-based-view-widget
class WritingForm(forms.ModelForm):
    
    choosen_answer = forms.ChoiceField( widget=forms.RadioSelect(),
                                       label='Choose answer',
                                       required=False)

    def __init__(self, question_object, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices_query = QuestionChoice.objects.filter(
                choice_to=question_object).order_by("?")
        
        #FIXME: Remove "lowest pk is correct" bug
        # Or remove pk from radio or random save correct answer

        self.RADIOCHOICES = [
            (obj.pk, obj.choice_text) 
            for obj in self.choices_query
        ]

        self.fields['choosen_answer'].choices = self.RADIOCHOICES

    class Meta:
        model = UserAnswer
        fields = ['choosen_answer']
