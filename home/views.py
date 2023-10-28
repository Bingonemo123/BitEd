from django.shortcuts import render
from django.template.loader import render_to_string

from tiles.loader import get_tiles_view, scroll_tiles_load
from home.ajax import is_ajax

from profile.models import Profile

from map.views import mapview_for_home
from django.http import HttpResponse
import json

# Create your views here.

def home_view (request, *args, **kwargs):
    if not is_ajax(request):
        context = {'template_tile' : render_to_string(
                    'tiles/base_tile_details.html',
                      context={"display": "d-none", "tile_id":"template_tile"},
                      request=request),} # 'tiles': get_tiles_view(request)
        if request.user.is_authenticated:
            profile = Profile.objects.filter(user=request.user).first()
            if profile is not None:
                context['balance'] = profile.k_balance
        
        context.update({'sidebar': mapview_for_home(request)})
        return render(request, 'home/home.html', context)
    else:
        # scroll
        if request.GET.get('mnode'):
            return mapview_for_home(request)
        else:
            return scroll_tiles_load(request)
        

def dark_mode(request):
    if is_ajax(request):
        request.session['theme'] = json.loads(request.body)['theme']

        return HttpResponse(status=204)



        
