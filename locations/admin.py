from django.contrib import admin
from .models import Location
from meal_categories.models import MealCategory
from meal_events.models import MealEvent
from meal_items.models import MealItem
from operating_hours.models import OperatingHour
from meal_reviews.models import Review

# Register your models here.
@admin.register(Location)
@admin.register(MealCategory)
@admin.register(MealEvent)
@admin.register(Review)
@admin.register(MealItem)
@admin.register(OperatingHour)
class AuthorAdmin(admin.ModelAdmin):
    pass