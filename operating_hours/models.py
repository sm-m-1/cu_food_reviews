from django.db import models

# Create your models here.
from locations.models import Location


class OperatingHour(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
