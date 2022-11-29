from django.db import models

# Create your models here.

class UserEvents(models.Model):
    event_title = models.CharField(max_length=1000)
    event_id = models.CharField(max_length=1000)
    event_name = models.CharField(max_length=1000)
    event_image = models.CharField(max_length=1000)
    event_date = models.CharField(max_length=1000)
    event_location = models.CharField(max_length=1000)
    event_price = models.CharField(max_length=1000)
    user_id = models.PositiveBigIntegerField()