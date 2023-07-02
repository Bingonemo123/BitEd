import sys, os, django
import random

sys.path.append(r"C:\Users\MSI\Documents\repos\BitEd") # here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bitedMainProject.settings")
django.setup()

# Now this script or any imported module can use any part of Django it needs.
from questions.models import Question
from questions.models import QuestionChoice
from django.db.models import Q
from writing.models import UserAnswer
from tiles.models import WriteRequestData
from tiles.models import Tile

from django.db.models import When, Case, Value
from django.db.models.functions import Length
from django.db.models import Subquery, OuterRef

from django.db.models import F
from django.db.models.lookups import Exact
from django.db.models import Exists

# my_answers =  UserAnswer.objects.filter(wrd__requested_by=1).order_by("-updated_at").values("answer_to", "answer_state", "pk")

# my_questions = []
# duplicates = []
# for a in my_answers:
#     if a["answer_to"] not in my_questions:
#         my_questions.append(a["answer_to"])
#     else:
#         duplicates.append(a["answer_to"])
# print(duplicates)                                


# u = (UserAnswer.objects.filter(wrd__requested_by=1)
#                 .order_by("answer_to", "-updated_at")
#                 .distinct("answer_to") 
#                 .annotate(correct=Case(When(answer_to__correct_choice = F("choosen_answer_obj"), then=True),default=False))
#                 .values("answer_to", "pk")
# )

# recent_answers = (UserAnswer.objects.filter(wrd__requested_by=1)
#                 .order_by("answer_to", "-updated_at")
#                 .distinct("answer_to") ).values_list("answer_state", flat=True)

# cor = 0
# incor = 0
# for x in recent_answers:
#     if x == 15:
#         cor += 1
#     elif x == 7:
#         incor += 1
# print('cor', cor)
# print('incor', incor)
# anot = recent_answers.annotate(
#     correct = F('answer_state').bitor(8),
#     incorrect = F('answer_state').bitand(~8)
# )
# print(anot.filter(answer_state = F("correct")).count())
# print(recent_answers.filter(answer_state =  15).count())

# print(anot.filter(answer_state = F("incorrect")).count())
# print(recent_answers.filter(answer_state =  7).count())


# print("TT", (UserAnswer.objects.filter(wrd__requested_by=1, answer_state = F('answer_state').bitor(8))
#                 .order_by("answer_to", "-updated_at")
#                 .distinct("answer_to") ).values_list("answer_state", flat=True).count())

# test = UserAnswer.objects.filter(answer_state = F('answer_state').bitor(1), pk__in= 
#     UserAnswer.objects.filter(wrd__requested_by=1)
#                 .order_by("answer_to", "-updated_at")
#                 .distinct("answer_to").values('pk')
# )

# incor = UserAnswer.objects.filter(answer_state = F('answer_state').bitand(~8), pk__in= 
#     UserAnswer.objects.filter(wrd__requested_by=1)
#                 .order_by("answer_to", "-updated_at")
#                 .distinct("answer_to").values('pk')
# )
# print("UU", test.count())


# print(recent_answers.filter(answer_state=F('answer_state').bitor(8)).count()) # corrects
# print(recent_answers.filter(answer_state=F('answer_state').bitand(~8)).count()) # inccorects

# print(recent_answers.filter(answer_state=F('answer_state').bitor(4)).count()) # Submitted
# print(recent_answers.filter(answer_state=F('answer_state').bitand(~4)).count())

# answers_io = (UserAnswer.objects.filter(wrd__requested_by=1)
#                     .order_by("answer_to", "-updated_at")
#                     .distinct("answer_to")
#                     ) 
# answers_oi = (UserAnswer.objects.filter(wrd__requested_by=self.request.user,
#                                                 answer_to__in = choosen_questions)
#                     .order_by("answer_to", "-updated_at")
#                     .distinct("answer_to").values('pk'))
import time 
import statistics


def test():
    return Question.objects.filter(
                    Exact(Subquery(
            UserAnswer.objects.filter(answer_to = OuterRef("pk"),
            wrd__requested_by = 1)
                            .order_by("-updated_at")
                            .values("answer_state")[:1])
                            .bitand(8), 8))


def test_1():
    mediator = Question.objects.annotate(latest_answer_state = Subquery(
                            UserAnswer.objects.filter(answer_to = OuterRef("pk"),
                            wrd__requested_by = 1)
                            .order_by("-updated_at")
                            .values("answer_state")[:1]))
    
    return mediator.filter(latest_answer_state = F('latest_answer_state').bitand(~8))

# timer = []

# while len(timer) < 100:
#     st = time.time()

#     list(test_1().values_list('pk', flat=True))
    
#     timer.append(time.time() - st)

# print('test_1', statistics.mean(timer))

q = test()
print(UserAnswer.objects.filter(answer_to = q[0])[0].answer_state)


# timer = []

# while len(timer) < 1000:
#     st = time.time()

#     obj = Tile.objects.get(pk=0)

#     choosen_questions = obj.questions.all()

#     choosen_questions |= Tile.objects.get(pk=2218).get_all_questions()

#     mediator = choosen_questions.annotate(latest_answer_state = Subquery(
#                                 UserAnswer.objects.filter(answer_to = OuterRef("pk"),
#                                 wrd__requested_by = 1)
#                                 .order_by("-updated_at")
#                                 .values("answer_state")[:1]))

#     quest = Question.objects.none()

#     quest |= mediator.filter(latest_answer_state = None)

#     list(quest.values_list('pk', flat=True))

#     # print(quest)
#     # print(UserAnswer.objects.filter(answer_to=quest[1]))
#     timer.append(time.time() - st)

# print(statistics.mean(timer))
# UserAnswer.objects.update(
#     answer_state = Case ( 
#                         When (
#                             Exact( 
#                                 Subquery(Question.objects.filter(pk=OuterRef("answer_to")).values("correct_choice")[:1]),
#                                 F("choosen_answer_obj") 
#                                  )
#                             , then=15 
#                             )
#                             , default=7    
#                          )
# )
# UserAnswer.objects.filter(pk = 2106).update(answer_state=16)
# h = UserAnswer.objects.filter(pk = 2106).annotate(
#     u = F('answer_state').bitand(~8)
# )
# print(h)
# print(h[0].answer_state, h[0].u)
# duplicate questions = 20563
# pk user answer 1942, 1862


# Question object (6996) Question object (6981) ?
# Question object (9566) Question object (9563) + 
# Question object (10146) Question object (10145) + 
# Question object (11948) Question object (11947) +


# Biostatistics 
# Questions without graphs
# user answer 1682
# 1822
# 2231

# without sound
# 1966

# order change user answer 1718 + 
# 1846 + 
