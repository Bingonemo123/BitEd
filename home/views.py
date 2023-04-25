from django.shortcuts import render

from tiles.loader import get_tiles_view, scroll_tiles_load
from home.ajax import is_ajax

from profile.models import Profile
from map.views import mapview_for_home
# Create your views here.

def home_view (request, *args, **kwargs):
    if not is_ajax(request):
        context = {'tiles': get_tiles_view(request)}
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

        
