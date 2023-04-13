from django.db import models
from tiles.models import WriteRequestData
from questions.models import Question
from questions.models import QuestionChoice

ANSWER_STATE = [
    (1, 'Unseen'),
    (2, 'Seen'),
    (4, 'Selected'),
    (8, 'Answered'),
    (16, 'Correct'),
    (32, 'Incorrect'),
    (64, 'Unselected Timeout'),
    (128, 'Selected Timeout')
]

# Create your models here.
# Junction Table between Questions and WRD
class UserAnswer(models.Model):
    wrd = models.ForeignKey(WriteRequestData, on_delete=models.CASCADE) # block id
    answer_to = models.ForeignKey(Question, on_delete=models.CASCADE)
    block_number = models.IntegerField(null=True) # number in block
    choosen_answer = models.IntegerField(null=True, blank=True)
    choosen_answer_obj = models.ForeignKey(QuestionChoice, 
                                        null=True, 
                                        blank=True,
                                        on_delete=models.CASCADE)
    answer_state = models.IntegerField(choices=ANSWER_STATE, default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



