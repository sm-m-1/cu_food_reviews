from django.db import models

# Create your models here.

from django.db import models


class Location(models.Model):
    c_id = models.BigIntegerField(null=True, unique=True)
    slug = models.SlugField(max_length=200, null=True)
    eatery_name = models.CharField(null=True)
    about = models.CharField(null=True)
    about_short = models.CharField(null=True)
    cornell_dining = models.BooleanField(default=True)
    op_hours_calc = models.CharField(null=True)
    op_hours_calc_desc = models.CharField(null=True)
    google_calendar_id = models.CharField(null=True)
    online_ordering = models.BooleanField(default=False)
    online_order_url = models.URLField(null=True)
    contact_phone = models.CharField(null=True)
    contact_email = models.EmailField(null=True)
    service_unit_id = models.BigIntegerField(null=True)
    campus_area = models.CharField(null=True)
    campus_area_short = models.CharField(null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    location_name = models.CharField(null=True)



