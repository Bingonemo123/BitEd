from django.contrib import admin

from .models import Question
from .models import QuestionChoice
# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    raw_id_fields = ['correct_choice', 'owner', 'next_question_in_group']


admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionChoice)
