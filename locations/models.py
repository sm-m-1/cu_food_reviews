# Create your models here.

from django.db import models
# from meal_items.models import MealItem


class Location(models.Model):
    c_id = models.BigIntegerField(null=True, unique=True)
    slug = models.SlugField(max_length=200, null=True, unique=True)
    eatery_name = models.CharField(null=True, max_length=200)
    eatery_name_short = models.CharField(null=True, max_length=100)
    about = models.TextField(null=True)
    about_short = models.TextField(null=True)
    cornell_dining = models.BooleanField(default=True)
    op_hours_calc = models.CharField(null=True, max_length=100)
    op_hours_calc_desc = models.TextField(null=True)
    google_calendar_id = models.CharField(null=True, max_length=200)
    online_ordering = models.BooleanField(default=False)
    online_order_url = models.URLField(null=True)
    contact_phone = models.CharField(null=True, max_length=30)
    contact_email = models.EmailField(null=True)
    service_unit_id = models.BigIntegerField(null=True)
    campus_area = models.CharField(null=True, max_length=100)
    campus_area_short = models.CharField(null=True, max_length=50)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    location_name = models.CharField(null=True, max_length=200)

    # def get_menus(self):
    #     return MealItem.objects.all()

    def __str__(self):
        return self.eatery_name
