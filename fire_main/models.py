from django.db import models

# Create your models here.
class fire_info(models.Model):
    latitude = models.TextField()
    longitude = models.TextField()
    city = models.TextField()
    country = models.TextField()
    brightness_temp = models.FloatField()
    frp = models.FloatField()

class fire_economic_data(models.Model):
    city = models.TextField(primary_key=True)
    country = models.TextField()
    details = models.TextField()
