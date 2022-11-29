from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserEvents(models.Model):
    event_id = models.CharField(max_length=1000)
    event_title = models.CharField(max_length=1000)
    event_image_url = models.CharField(max_length=1000)
    event_date = models.CharField(max_length=1000)
    event_location = models.CharField(max_length=1000)
    event_price = models.CharField(max_length=1000)
    user_id = models.PositiveBigIntegerField()

class User(AbstractUser):
    zip = models.PositiveBigIntegerField()