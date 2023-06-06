import sys, os, django
import random

sys.path.append(r"C:\Users\MSI\Documents\repos\BitEd") #here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bitedMainProject.settings")
django.setup()

# Now this script or any imported module can use any part of Django it needs.
from questions.models import Question
from questions.models import QuestionChoice
from django.db.models import Q


print(Question.objects.filter(next_question_in_group__isnull=False).values_list('id', 'next_question_in_group'))


# answers_with = QuestionChoice.objects.filter(Q(choice_text__icontains="\t\t\t\t") )

# qs = list(set([ans.choice_to for ans in answers_with]))
# print(len(qs))


# Question object (6996) Question object (6981) ?
# Question object (9566) Question object (9563) + 
# Question object (10146) Question object (10145) + 
# Question object (11948) Question object (11947) +


# Biostatistics 
# Questions without graphs
# user answer 1682
# 1822

# order change user answer 1718 + 
#
