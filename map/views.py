from django.views.generic import TemplateView
from folder.models import Folder
from home.ajax import is_ajax
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.http import HttpResponse
from django.template.loader import render_to_string

# Create your views here.


class MapView(TemplateView):
    template_name = 'map/folder_map.html'

    def get(self, request, *args, **kwargs):
        if is_ajax(request):
            folder_pk = int(request.GET.get('mnode')[13:])
            folder_obj = get_object_or_404(Folder, pk=folder_pk)
            children_set = Folder.objects.filter(parent=folder_obj)
            data = serializers.serialize('json', list(children_set))
            print(data)
            return HttpResponse(data)
        return super().get(request, *args, **kwargs)


def mapview_for_home(request):
    template_name = 'map/home_map.html'

    if is_ajax(request):
        folder_pk = int(request.GET.get('mnode')[13:])
        folder_obj = get_object_or_404(Folder, pk=folder_pk)
        children_set = Folder.objects.filter(parent=folder_obj)
        data = serializers.serialize('json', list(children_set))
        return HttpResponse(data)
    return render_to_string(template_name, request=request)
