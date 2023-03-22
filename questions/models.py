from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator

User = get_user_model()


# Create your models here.
class Question (models.Model):
    question_title = models.CharField(max_length=150)
    question_body = models.TextField()
    question_explanation = models.TextField()

    correct_choice = models.ForeignKey('QuestionChoice',null=True, blank=True, on_delete=models.SET_NULL)

    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class QuestionChoice (models.Model):
    choice_to = models.ForeignKey(Question, null=True, 
                                            blank=True, 
                                            on_delete=models.CASCADE)
    choice_text = models.TextField(validators=[MinLengthValidator(1)])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
