from django.shortcuts import render
from django.views.generic import ListView
from locations.models import Location
# Create your views here.

class LocationList(ListView):
    model = Location
    template_name = 'location-list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        # print("context: ", context)
        return context





