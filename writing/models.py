from django.db import models
from tiles.models import WriteRequestData
from questions.models import Question
from questions.models import QuestionChoice

ANSWER_STATE = [
    (1, 'Seen'), # Unseen
    (2, 'Selected'), # Not Selected (Not Submitted)
    (4, 'Submitted'), # Not Submited ( Not answered )
    (8, 'Correct'), # Incorrect
    (16, 'Timeout') # Answered Timely
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
    answer_state = models.IntegerField(choices=ANSWER_STATE, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



