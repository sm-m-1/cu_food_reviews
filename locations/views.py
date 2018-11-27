from django.shortcuts import render
from django.views.generic import ListView
from rest_framework.response import Response

from locations.models import Location
from locations.serializers import LocationListSerializer
from meal_categories.models import MealCategory
from operating_hours.models import OperatingHour
from meal_events.models import MealEvent
from meal_items.models import MealItem
from rest_framework.views import APIView
from rest_framework import routers, serializers, viewsets, generics, renderers


# Create your views here.

class LocationsApiView(generics.ListAPIView):
    queryset = Location.objects.all()
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = LocationListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        date = self.kwargs['date']
        print("date:", date)
        return super().get_queryset()


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
            info['meal_event'] = MealEvent.objects.filter(operating_hour__date=date, operating_hour__location=location)
            info['meal_category'] = MealEvent.objects.filter()

            # info['meal_items'] = MealItem.objects.filter(meal_category__meal_event__operating=)
            object_list_new.append(info)
        context['object_list'] = object_list_new
        # print("context: ", context)
        return context

    def get_queryset(self):
        query = super().get_queryset()
        # print("query:", query)
        return query








