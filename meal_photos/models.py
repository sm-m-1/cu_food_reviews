import os
import random

from django.db import models

# Create your models here.
from meal_items.models import MealItem

def upload_image_path(instance, filename):
    # print("instance", instance)
    # print("filename", filename)
    new_filename = random.randint(1,3910209312)
    name, ext = os.path.splitext(os.path.basename(filename))
    final_filename = '{new_name}{ext}'.format(new_name=new_filename, ext=ext)
    return "products/{new_filename}/{final_filename}".format(
        new_filename=new_filename, final_filename=final_filename
    )

class Photo(models.Model):
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    meal_item = models.ForeignKey(MealItem, on_delete=models.CASCADE)
    liked = models.IntegerField(null=True, blank=True)
