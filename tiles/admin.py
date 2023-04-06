from django.contrib import admin

# Register your models here.
from tiles.models import WriteRequestData
from tiles.models import Tile

admin.site.register(WriteRequestData)
admin.site.register(Tile)
