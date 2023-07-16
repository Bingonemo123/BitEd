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


a= list(Question.objects.filter(question_body__contains="Item 2 of 2")) 
b = list(Question.objects.filter(question_explanation__contains="A 65-year-old man"))

print(list(set(a) & set(b)))

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
