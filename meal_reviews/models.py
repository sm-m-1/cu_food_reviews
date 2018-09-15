from django.conf import settings
from django.db import models
from datetime import datetime

# Create your models here.
from meal_items.models import MealItem

class Review(models.Model):
    comment = models.TextField(null=True)
    date_created = models.DateTimeField(default=datetime.now)
    rating = models.IntegerField(default=4)
    menu_item = models.ForeignKey(MealItem, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)