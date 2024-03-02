import sys
import os
import django
from datetime import datetime
from datetime import timedelta

sys.path.append(r"C:\Users\MSI\Documents\repos\BitEd")
# here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bitedMainProject.settings")
django.setup()

from folder.models import Folder  # noqa: E402
# Now this script or any imported module can use any part of Django it needs.

fund = Folder.objects.filter(created_at__gte=datetime.now()
                             - timedelta(days=30))
for mobj in fund:
    print(mobj, "deleted")
    mobj.delete()

