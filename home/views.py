'''Home Page Displaying Main Module'''
# from django.template.loader import render_to_string

# from tiles.loader import get_tiles_view,
import json
from profile.models import Profile
from django.shortcuts import render
from django.http import HttpResponse
from home.ajax import is_ajax


from map.views import mapview_for_home

# Create your views here.


def home_view(request):
    '''Home page main Function '''
    if not is_ajax(request):
        context = {}  # 'tiles': get_tiles_view(request)
        if request.user.is_authenticated:
            profile = Profile.objects.filter(user=request.user).first()
            if profile is not None:
                context['balance'] = profile.k_balance
        context.update({'sidebar': mapview_for_home(request)})
        return render(request, 'home/home.html', context)
    else:
        # subject expolorer
        if request.GET.get('mnode'):
            return mapview_for_home(request)


def dark_mode(request):
    '''Function to activate dark mode'''
    if is_ajax(request):
        request.session['theme'] = json.loads(request.body)['theme']

        return HttpResponse(status=204)
