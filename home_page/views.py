from http.client import HTTPResponse
from django.shortcuts import render

from django.http import HttpResponse
from home_page_tiles.views import get_tiles_view, scroll_tiles_load

from user_accounts.models import Profile
# Create your views here.


# https://stackoverflow.com/questions/63629935/django-3-1-and-is-ajax
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def load_home_page (request, *args, **kwargs):
    if not is_ajax(request):
        context = {'tiles': get_tiles_view(request)}
        if request.user.is_authenticated:
            profile = Profile.objects.filter(user=request.user).first()
            if profile is not None:
                context['balance'] = profile.k_balance
        return render(request, 'home_page/home.html', context)
    else:
        # scroll
        return scroll_tiles_load(request)

        # javascript set header
