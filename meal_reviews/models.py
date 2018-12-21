from django.contrib.auth import get_user_model
from django.db import models
from datetime import datetime

# Create your models here.
from meal_items.models import MealItem

class Review(models.Model):
    comment = models.TextField(null=True)
    created_on = models.DateTimeField(default=datetime.now)
    rating = models.IntegerField(default=4, null=True)
    menu_item = models.ForeignKey(MealItem, on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)