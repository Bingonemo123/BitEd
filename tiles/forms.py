from django import forms
from django.core.exceptions import ValidationError
from tiles.models import BLOCK_MODE_CHOICES
from tiles.models import BLOCK_SECTOR_CHOICES
from questions.models import Question
from tiles.rand import get_random_questions

class writeRequestDataForm(forms.Form):
    block_mode = forms.ChoiceField(choices=BLOCK_MODE_CHOICES)
    block_total_questions = forms.IntegerField(initial=40)
    sector = forms.ChoiceField(choices=BLOCK_SECTOR_CHOICES)
    timed = forms.BooleanField(required=False)

    def clean_block_total_questions(self):
        questions_query_set = Question.objects        
        self.random_questions = get_random_questions(questions_query_set, 
                                   self.cleaned_data['block_total_questions'])
        if self.random_questions is None:
            raise ValidationError('Not Enough Questions in Database', code='invalid')
        else:
            return self.cleaned_data['block_total_questions']
