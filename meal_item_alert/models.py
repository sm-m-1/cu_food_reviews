from django.db import models
from django.contrib.auth import get_user_model

from meal_items.models import MealItem


class Alert(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False)
    meal_item = models.ForeignKey(MealItem, on_delete=models.CASCADE, null=False)
    active = models.BooleanField(null=False)

    def __str__(self):
        return "{} at {}".format( self.meal_item.name, str(self.meal_item.meal_location) )