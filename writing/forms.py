from django import forms
from django.db import models

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


#https://stackoverflow.com/questions/3464758/how-should-i-represent-a-bit-flags-int-field-in-django-admin
# class BitFlagFormField(forms.MultipleChoiceField):
#     widget = forms.CheckboxSelectMultiple

#     def __init__(self, *args, **kwargs):
#         super(BitFlagFormField, self).__init__(*args, **kwargs)

# class BitFlagField(models.Field):
#     __metaclass__ = models.SubfieldBase

#     def get_internal_type(self):
#         return "Integer"

#     def get_choices_default(self):
#         return self.get_choices(include_blank=False)

#     def _get_FIELD_display(self, field):
#         value = getattr(self, field.attname)
#         choicedict = dict(field.choices)

#     def formfield(self, **kwargs):
#         # do not call super, as that overrides default widget if it has choices
#         defaults = {'required': not self.blank, 'label': capfirst(self.verbose_name), 
#                     'help_text': self.help_text, 'choices':self.choices}
#         if self.has_default():
#             defaults['initial'] = self.get_default()
#         defaults.update(kwargs)
#         return BitFlagFormField(**defaults)

#     def get_db_prep_value(self, value):
#         if isinstance(value, int):
#             return value
#         elif isinstance(value, list):
#             return sum(value)

#     def to_python(self, value):
#         result = []
#         n = 1
#         while value > 0:
#             if (value % 2) > 0:
#                 result.append(n)
#             n *= 2
#             value /= 2
#         return sorted(result)


#     def contribute_to_class(self, cls, name):
#         super(BitFlagField, self).contribute_to_class(cls, name)
#         if self.choices:
#             func = lambda self, fieldname = name, choicedict = dict(self.choices):" and ".join([choicedict.get(value,value) for value in getattr(self,fieldname)])
#             setattr(cls, 'get_%s_display' % self.name, func)
