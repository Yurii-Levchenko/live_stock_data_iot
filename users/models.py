from django.db import models
from django.contrib.auth.models import User
from dashboard.models import Stock

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    favorite_tickers = models.ManyToManyField(Stock, blank=True, related_name='favorite')

    def __str__(self):
        return self.user.username