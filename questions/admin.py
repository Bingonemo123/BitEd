from django.contrib import admin

from .models import Question
from .models import QuestionChoice

from django.utils.html import format_html
# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    list_display  = ["question_title"]
    raw_id_fields = ['correct_choice', 'owner', 'next_question_in_group']

    readonly_fields = ['preview']

    def preview(self, obj):
        return format_html('<a href="/question/preview/{}">Preview Question</a>'.format(obj.pk))  # however you generate the link

admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionChoice)
