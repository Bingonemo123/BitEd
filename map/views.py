from django.views.generic import TemplateView
from tiles.models import Tile
from home.views import is_ajax
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.http import HttpResponse

# Create your views here.

class MapView(TemplateView):
    template_name = 'map/tile_map.html'

    def get(self, request, *args, **kwargs):
        if is_ajax(request):
            tile_pk = int(request.GET.get('mnode')[5:])
            tile_obj = get_object_or_404(Tile, pk=tile_pk)
            children_set = Tile.objects.filter(parent=tile_obj)
            data = serializers.serialize('json', list(children_set))
            return HttpResponse(data)
        return super().get(request, *args, **kwargs)



