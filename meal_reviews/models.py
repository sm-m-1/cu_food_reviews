from django.contrib.auth import get_user_model
from django.db import models
from datetime import datetime

# Create your models here.
from django.urls import reverse

from meal_items.models import MealItem

class Review(models.Model):
    comment = models.TextField(null=True)
    created_on = models.DateTimeField(default=datetime.now)
    rating = models.IntegerField(null=False)
    menu_item = models.ForeignKey(MealItem, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "{} at {}".format(self.menu_item.name, str(self.menu_item.meal_location)[:20])

    def get_delete_url(self):
        return reverse("review_item_delete", kwargs={"id": self.id})

    def get_update_url(self):
        return reverse("review_item_update", kwargs={"id": self.id})
