from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class WeatherStation(models.Model):
    id = models.CharField(max_length=35,primary_key=True)
    neighborhood = models.CharField(max_length=35)

class Subscriber(models.Model):
    user = models.ForeignKey(User)
    station = models.ForeignKey(WeatherStation)
