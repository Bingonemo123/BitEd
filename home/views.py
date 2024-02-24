'''Home Page Displaying Main Module'''
# from django.template.loader import render_to_string

# from folders.loader import get_folders_view,
import json
from profile.models import Profile
from django.shortcuts import render
from django.http import HttpResponse
from home.ajax import is_ajax
import os

from map.views import mapview_for_home

# Create your views here.


def home_view(request):
    '''Home page main Function '''
    if not is_ajax(request):
        context = {}  # 'folders': get_folders_view(request)
        if request.user.is_authenticated:
            profile = Profile.objects.filter(user=request.user).first()
            if profile is not None:
                context['balance'] = profile.k_balance
        # context.update({'sidebar': mapview_for_home(request)})
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
    
import os
import os
from django.shortcuts import redirect, HttpResponse
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

def google_auth(request):
    try:
        # Instantiate the OAuth2Client
        client = OAuth2Client(
            request=request,
            consumer_key=os.getenv('GOOGLE_OAUTH2_CLIENT_ID'),
            consumer_secret=os.getenv('GOOGLE_OAUTH2_CLIENT_SECRET'),
            access_token_method='POST',
            access_token_url='https://accounts.google.com/o/oauth2/token',
            callback_url='http://127.0.0.1:8000/accounts/google/login/callback/',
            scope=['email', 'profile'],
            scope_delimiter=' ',
        )

        # Redirect users to Google's authentication URL
        authorization_url = 'https://accounts.google.com/o/oauth2/auth'
        extra_params = {}
        redirect_url = client.get_redirect_url(authorization_url, extra_params)
        return redirect(redirect_url)
    except Exception as e:
        print(e)
        # Handle the error gracefully (e.g., display a friendly error message to the user)
        return HttpResponse("An error occurred during authentication. Please try again later.", status=500)