import sys
import os
import django
from datetime import datetime
from datetime import timezone
from datetime import timedelta

sys.path.append(r"C:\Users\MSI\Documents\repos\BitEd")
# here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bitedMainProject.settings")
django.setup()

from folder.models import Folder  # noqa: E402
# Now this script or any imported module can use any part of Django it needs.

fund = Folder.objects.filter(created_at__lte=datetime.now(timezone.utc)
                             - timedelta(minutes=30))

print(fund)
print(datetime.utcnow())
print(Folder.objects.order_by("?").first().created_at)
for mobj in fund:
    mobj.delete()

