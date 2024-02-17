import sys
import os
import django
from datetime import datetime
from datetime import timedelta

sys.path.append(r"C:\Users\MSI\Documents\repos\BitEd")
# here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bitedMainProject.settings")
django.setup()

from questions.models import Question
# Now this script or any imported module can use any part of Django it needs.



fund = Question.objects.filter(created_at__gte=datetime.now() - timedelta(days=1))
for mobj in fund:
    mobj.delete()
