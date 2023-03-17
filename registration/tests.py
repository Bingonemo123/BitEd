from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class TestLoginReverse(TestCase):

    def test_login_reverse(self):
        login_url = reverse('login')
        print(login_url)
