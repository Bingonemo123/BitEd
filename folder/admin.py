from django.contrib import admin

# Register your models here.
from folder.models import WriteRequestData
from folder.models import Folder

admin.site.register(WriteRequestData)
admin.site.register(Folder)
