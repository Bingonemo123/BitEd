from django.contrib import admin

from .models import Question
from .models import QuestionChoice
# Register your models here.

admin.site.register(Question)
admin.site.register(QuestionChoice)
