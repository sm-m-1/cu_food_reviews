from datetime import datetime, timedelta
from django.db.models import Prefetch
from django.shortcuts import render
from django.views.generic import ListView

from locations.models import Location
from meal_categories.models import MealCategory
from meal_events.models import MealEvent
from meal_items.models import MealItem


class LocationList(ListView):
    model = Location
    template_name = 'location-list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        today = datetime.now().date()
        # today = datetime(2018,12,20).date()
        date = self.request.GET.get('date', today.isoformat())
        open_today = self.request.GET.get('open_today')

        object_list_old = context['object_list']
        object_list_new = []

        locations = self.get_queryset().prefetch_related('operatinghour_set', 'operatinghour_set__mealevent_set')
        events = MealEvent.objects.filter(operating_hour__date=date).select_related('operating_hour', 'operating_hour__location')
        categories = MealCategory.objects.all().prefetch_related('meal_event')
        items = MealItem.objects.all().order_by('name').prefetch_related('meal_category', 'meal_category__meal_event','meal_location', 'review_set')
        #
        # events = MealEvent.objects.filter(operating_hour__date=date)
        # categories = MealCategory.objects.all()
        # items = MealItem.objects.all()

        for location in locations:
            info = {
                'location': location,
                'location_data': [],
                'dining_items': [],
            }
            # meal_events = location.operatinghour_set.all()
            # meal_events = events.filter(operating_hour__location=location)
            meal_events = []
            for event in events:
                if event.operating_hour.location == location:
                    meal_events.append(event)

            if open_today == 'on' and len(meal_events) == 0: continue  # skip location that is closed today

            for event in meal_events:
                # meal_categories = [ category for category in categories if category.meal_event == event ]
                meal_categories = [ category for category in categories if category.meal_event == event ]
                meal_category_data = []
                for category in meal_categories:
                    data = {
                        'category': category,
                        # 'category_items': items.filter(meal_category=category, meal_location=location, meal_category__meal_event=event)
                        'category_items': []
                    }
                    for meal_item in items:
                        if meal_item.meal_category == category and meal_item.meal_location == location and meal_item.meal_category.meal_event == event:
                            data['category_items'].append(meal_item)

                    meal_category_data.append(data)

                data = {
                    'event': event,
                    'meal_category_data': meal_category_data
                }
                info['location_data'].append(data)

                # dining_items = items.filter(meal_location=location, is_dining_item=True)
                dining_items = []
                for meal_item in items:
                    if meal_item.meal_location == location and meal_item.is_dining_item == True:
                        dining_items.append(meal_item)
                info['dining_items'] = dining_items

            object_list_new.append(info)


        # for location in object_list_old:
        #     info = {
        #         'location': location,
        #         'location_data': [],
        #         'dining_items': [],
        #     }
        #     meal_events = MealEvent.objects.filter(operating_hour__date=date, operating_hour__location=location)
        #
        #     if open_today == 'on' and meal_events.exists() == False: continue # skip location that is closed today
        #
        #     for event in meal_events:
        #         meal_categories = MealCategory.objects.filter(meal_event=event)
        #         meal_category_data = []
        #         for category in meal_categories:
        #             data = {
        #                 'category': category,
        #                 'category_items': MealItem.objects.filter(
        #                     meal_category__meal_event=event,
        #                     meal_category=category,
        #                     meal_location=location
        #                 ).order_by('name')
        #             }
        #             meal_category_data.append(data)
        #
        #         data = {
        #             'event': event,
        #             'meal_category_data': meal_category_data
        #         }
        #         info['location_data'].append(data)
        #
        #     dining_items = MealItem.objects.filter(meal_location=location, is_dining_item=True).order_by('name')
        #     info['dining_items'] = dining_items
        #     object_list_new.append(info)

        context['object_list'] = object_list_new
        next_seven_days = [( today + timedelta(days=i) ).isoformat() for i in range(7)]
        context['date_list'] = next_seven_days

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






