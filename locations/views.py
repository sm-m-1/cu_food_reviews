from django.shortcuts import render
from django.views.generic import ListView
from rest_framework.response import Response

from locations.models import Location
from locations.serializers import LocationListSerializer
from meal_categories.models import MealCategory
from operating_hours.models import OperatingHour
from meal_events.models import MealEvent
from meal_items.models import MealItem
from datetime import datetime, timedelta, date
from rest_framework.views import APIView
from rest_framework import routers, serializers, viewsets, generics, renderers


class LocationList(ListView):
    model = Location
    template_name = 'location-list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        # print("context: ", context)
        date = self.request.GET.get('date', '2018-12-01')
        # print("self.kwargs['date']", date)
        # print("type(date):", type(date))
        object_list_old = context['object_list']
        object_list_new = []
        for location in object_list_old:
            info = {
                'location': location,
                'location_data': [],
                'dining_items': [],
            }
            meal_events = MealEvent.objects.filter(operating_hour__date=date, operating_hour__location=location)
            # print("meal_events: ", meal_events)
            for event in meal_events:
                meal_categories = MealCategory.objects.filter(meal_event=event)
                meal_category_data = []
                for category in meal_categories:
                    # meal_category_data['category'] = category
                    # meal_category_data['category_data'] = MealCategory.objects.filter(meal_event=event)
                    data = {
                        'category': category,
                        'category_items': MealItem.objects.filter(
                            meal_category__meal_event=event,
                            meal_category=category,
                            meal_location=location
                        )
                    }
                    meal_category_data.append(data)

                    # menu_items = MealItem.objects.filter(meal_category__meal_event=event, meal_category=category)

                data = {
                    'event': event,
                    'meal_category_data': meal_category_data
                }
                info['location_data'].append(data)

            dining_items = MealItem.objects.filter(meal_location=location, is_dining_item=True)
            info['dining_items'] = dining_items
            object_list_new.append(info)
            # break
        context['object_list'] = object_list_new
        # print("context: ", context)
        temp_start_date = "2018-12-01"
        start_date = datetime.strptime(temp_start_date, "%Y-%m-%d").date()
        # end_date = start_date + timedelta(days=7)
        next_seven_days = [( start_date + timedelta(days=i) ).isoformat() for i in range(7)]
        # context['start_date'] = start_date.isoformat()
        # context['end_date'] = end_date.isoformat()
        context['date_list'] = next_seven_days
        if self.request.user.is_authenticated:
            context['authenticated_user'] = self.request.user.username
        return context

    def get_queryset(self):
        query = super().get_queryset()
        area_name = self.request.GET.get('campus_area_short', 'North')
        query = query.filter(campus_area_short__icontains=area_name)
        if area_name: query = query.order_by('-eatery_name')
        # print("self.request.GET:", self.request.GET)
        return query



# django rest framework simple view.
# class LocationsApiView(generics.ListAPIView):
#     queryset = Location.objects.all()
#     renderer_classes = (renderers.JSONRenderer,)
#     serializer_class = LocationListSerializer
#
#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def get_queryset(self):
#         date = self.kwargs['date']
#         print("date:", date)
#         return super().get_queryset()








