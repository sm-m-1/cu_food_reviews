from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from meal_items.models import MealItem


class Alert(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False)
    meal_item = models.ForeignKey(MealItem, on_delete=models.CASCADE, null=False)
    active = models.BooleanField(null=False)

    def __str__(self):
        return "{} at {}".format( self.meal_item.name, str(self.meal_item.meal_location) )

    def get_delete_url(self):
        # return "/products/{slug}/".format(slug=self.slug)
        return reverse("meal_item_alert_delete", kwargs={"id": self.id})


def user_did_not_create_alert_for_item(user, meal_item):
    return not Alert.objects.filter(user=user, meal_item=meal_item).exists()