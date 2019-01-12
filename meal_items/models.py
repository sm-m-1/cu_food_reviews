import random
import string

from django.db import models
from django.db.models import Avg
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
from locations.models import Location
from meal_categories.models import MealCategory


class MealItem(models.Model):
    name = models.CharField(null=True, max_length=100)
    slug = models.SlugField(max_length=200, null=True, unique=True)
    description = models.CharField(null=True, max_length=200)
    is_healthy = models.BooleanField(default=False)
    sort_index = models.IntegerField(null=True)
    meal_category = models.ManyToManyField(MealCategory)
    meal_location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    is_dining_item = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # return "/products/{slug}/".format(slug=self.slug)
        return reverse("meal_item", kwargs={"item_slug": self.slug})

    def get_average_rating(self):
        return self.review_set.aggregate(Avg('rating')).get('rating__avg')

    def get_rating_count(self):
        return self.review_set.count()


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance, new_slug=None):
    # print("instance: ", instance.eatery_name)
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)

    return slug

@receiver(pre_save, sender=MealItem)
def meal_item_pre_save_handler(sender, instance, *args, **kwargs):
    # print("sender: ", sender)
    # print("instance: ", instance)
    # print("args: ", args)
    # print("kwargs: ", kwargs)
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

# pre_save.connect(location_pre_save_receiver, sender=Location)