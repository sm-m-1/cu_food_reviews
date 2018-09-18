from django.shortcuts import render
from django.views.generic import ListView
from locations.models import Location
from meal_categories.models import MealCategory
from operating_hours.models import OperatingHour
from meal_events.models import MealEvent
from meal_items.models import MealItem
# Create your views here.

class LocationList(ListView):
    model = Location
    template_name = 'location-list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        # print("context: ", context)
        date = self.kwargs['date']
        # print("self.kwargs['date']", date)
        # print("type(date):", type(date))
        object_list_old = context['object_list']
        object_list_new = []
        for location in object_list_old:
            info = {}
            info['location'] = location
            events = MealEvent.objects.filter(operating_hour__date=date, operating_hour__location=location)
            for event in events:
                menu = []
                categories = MealCategory.objects.filter(meal_event=event)
                print("categories: ", categories)

            # info['meal_items'] = MealItem.objects.filter(meal_category__meal_event__operating=)
            object_list_new.append(info)
        context['object_list'] = object_list_new
        # print("context: ", context)
        return context

    def get_queryset(self):
        query = super().get_queryset()
        # print("query:", query)
        return query








