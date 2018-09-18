from django.db import models

# Create your models here.
from locations.models import Location


class OperatingHour(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    location = models.ManyToManyField(Location)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.

    def __str__(self):
        return "Date: {}".format(self.date.isoformat())


