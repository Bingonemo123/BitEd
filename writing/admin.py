from django.contrib import admin

from .models import UserAnswer
# Register your models here.


class UserAnswerAdmin(admin.ModelAdmin):

    raw_id_fields = ['wrd', 'answer_to', 'choosen_answer_obj']

admin.site.register(UserAnswer, UserAnswerAdmin)
