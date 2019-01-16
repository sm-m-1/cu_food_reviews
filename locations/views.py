from datetime import timedelta, date
from django.db.models import Avg
from django.db.models import Count
from django.shortcuts import render
from django.views.generic import ListView
from django.core.cache import cache

from locations.models import Location
from meal_categories.models import MealCategory
from meal_events.models import MealEvent
from meal_items.models import MealItem


class LocationList(ListView):
    model = Location
    template_name = 'location-list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        today = self.request.GET.get('date', date.today().isoformat())
        open_today = self.request.GET.get('open_today')
        location_data_cache = cache.get(self.request.get_full_path())
        if location_data_cache:
            context['object_list'] = location_data_cache
            context['date_list'] = [( date.today() + timedelta(days=i) ).isoformat() for i in range(7)]
            return context

        object_list_old = context['object_list']
        object_list_new = []
        for location in object_list_old: # build the location data
            info = {
                'location': location,
                'location_data': [],
                'dining_items': [],
            }
            meal_events = MealEvent.objects.filter( # choose the meal events for this location.
                operating_hour__date=today, operating_hour__location=location
            ).order_by('start_timestamp')

            if open_today == 'on' and meal_events.exists() == False: continue  # skip location that is closed today

            for event in meal_events: # build the location meal events data
                meal_categories = MealCategory.objects.filter(meal_event=event)
                meal_category_data = []
                for category in meal_categories: # build the location meal category data
                    data = {
                        'category': category,
                        'category_items': MealItem.objects.filter( # build the location meal items data for the category.
                            meal_category__meal_event=event,
                            meal_category=category,
                            meal_location=location
                        ).order_by('name').annotate(
                            rating_count=Count('review'),
                            avg_rating=Avg('review__rating')
                        )
                    }
                    meal_category_data.append(data) # save the location meal items data.

                data = {
                    'event': event,
                    'meal_category_data': meal_category_data
                }
                info['location_data'].append(data) # save the location meal category data

            dining_items = MealItem.objects.filter( # build the extra dining items for the location
                meal_location=location, is_dining_item=True).order_by('name').annotate(
                rating_count=Count('review'),
                avg_rating=Avg('review__rating')
            )
            info['dining_items'] = dining_items
            object_list_new.append(info) # save the full location data to the object_list

        context['object_list'] = object_list_new
        context['date_list'] = [( date.today() + timedelta(days=i) ).isoformat() for i in range(7)]
        cache.set(self.request.get_full_path(), object_list_new, 600) # 10 minute cache
        return context



    def get_queryset(self):
        # queryset of the location model
        query = super().get_queryset().order_by('-eatery_name')
        area_name = self.request.GET.get('campus_area_short', 'All') # Choosing All as default when nothing is provided
        if area_name == 'All': return query
        query = query.filter(campus_area_short__icontains=area_name)
        return query


def privacy_page(request):
    return render(request, template_name='privacy.html')






