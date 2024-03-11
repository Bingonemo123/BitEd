# views.py

import requests
from django.shortcuts import redirect
from django.conf import settings

def google_oauth_login(request):
    # Construct the URL for Google OAuth
    google_oauth_url = (
        f"https://accounts.google.com/o/oauth2/auth?"
        f"client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=email profile openid"
    )

    # Redirect the user to the Google OAuth URL
    return redirect(google_oauth_url)
