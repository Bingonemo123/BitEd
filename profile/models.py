from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

# https://docs.djangoproject.com/en/4.1/topics/auth/default/
User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    k_balance = models.FloatField(default=100)

    def __str__(self):
        return self.user.username
