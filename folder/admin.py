from django.contrib import admin

# Register your models here.
from folder.models import WriteRequestData
from folder.models import Folder


class FolderAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(WriteRequestData)
admin.site.register(Folder, FolderAdmin)
