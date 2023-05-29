import sys, os, django
import random

sys.path.append(r"C:\Users\MSI\Documents\repos\BitEd") #here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bitedMainProject.settings")
django.setup()

# Now this script or any imported module can use any part of Django it needs.
from tiles.models import Tile
from tiles.rand import get_random_questions
from tiles.rand import random_questions_random_sample

root = Tile.objects.get(pk=0)

import time

allqs = root.get_all_questions()

st = time.time()
r1 = get_random_questions(allqs, 40)
print(time.time() -st, len(r1))

st = time.time()
r1 = random_questions_random_sample(allqs, 40)
print(time.time() -st, r1.count())






# print(get_random_questions(allq, 40))
