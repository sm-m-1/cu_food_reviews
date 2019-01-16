from django.contrib.auth import get_user_model
from django.db import models
from datetime import datetime

# Create your models here.
from django.urls import reverse

from meal_items.models import MealItem

class Review(models.Model):
    comment = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(default=datetime.now)
    rating = models.IntegerField(null=False)
    meal_item = models.ForeignKey(MealItem, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "{} at {}".format(self.meal_item.name, str(self.meal_item.meal_location)[:27])

    def get_delete_url(self):
        return reverse("review_item_delete", kwargs={"id": self.id})

    def get_update_url(self):
        return reverse("review_item_update", kwargs={"id": self.id})

def user_has_not_reviewed_item(user, meal_item):
    return not Review.objects.filter(user=user, meal_item=meal_item).exists()
