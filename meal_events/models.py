from django.db import models

# Create your models here.
from operating_hours.models import OperatingHour

class MealEvent(models.Model):
    description = models.TextField(null=True)
    start_timestamp = models.BigIntegerField(null=True)
    end_timestamp = models.BigIntegerField(null=True)
    start_time = models.CharField(null=True, max_length=50)
    end_time = models.CharField(null=True, max_length=50)
    operating_hour = models.ForeignKey(OperatingHour, on_delete=models.CASCADE)