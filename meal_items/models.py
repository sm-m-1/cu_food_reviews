from django.db import models

# Create your models here.
from locations.models import Location
from meal_categories.models import MealCategory


class MealItem(models.Model):
    name = models.CharField(null=True, max_length=100)
    description = models.CharField(null=True, max_length=200)
    is_healthy = models.BooleanField(default=False)
    sort_index = models.IntegerField(null=True)
    meal_category = models.ManyToManyField(MealCategory)
    meal_location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    is_dining_item = models.BooleanField(default=False)

    def __str__(self):
        return self.name