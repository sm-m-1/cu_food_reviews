from django.db import models

# Create your models here.
from meal_events.models import MealEvent


class MealCategory(models.Model):
    name = models.CharField(null=True, max_length=100)
    sort_index = models.IntegerField(null=True)
    meal_event = models.ManyToManyField(MealEvent)

    def __str__(self):
        return self.name