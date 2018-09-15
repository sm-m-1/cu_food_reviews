from django.core.management.base import BaseCommand, CommandError

from django.core.management.base import BaseCommand, CommandError
import json
import urllib.request

from locations.models import Location
from meal_events.models import MealEvent
from meal_categories.models import MealCategory
from meal_items.models import MealItem
from operating_hours.models import OperatingHour


API_ENDPOINT_URL = "https://now.dining.cornell.edu/api/1.0/dining/eateries.json"


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        response = load_data_from_api_endpoint(API_ENDPOINT_URL)
        data = response.get('data')
        locations = data.get('eateries')
        first_loc = locations[0]
        for location in locations:
            created_location = create_location(location)
            operating_hours = location.get('operatingHours')
            for item in operating_hours:
                date = item.get('date')
                create_operating_hour(date, created_location)

        pass

def load_data_from_api_endpoint(api_url):
    page = urllib.request
    contents = json.load(urllib.request.urlopen(api_url))
    return contents


def create_location(location_info):
    location_object = Location.objects.get_or_create(c_id=location_info.get('id'))
    location = location_object[0]

    location.slug = location_info.get('slug')
    location.eatery_name = location_info.get('name')
    location.eatery_name_short = location_info.get('nameshort')
    location.about = location_info.get('about')
    location.about_short = location_info.get('aboutshort')
    location.cornell_dining = location_info.get('cornellDining')
    location.op_hours_calc = location_info.get('opHoursCalc')
    location.op_hours_calc_desc = location_info.get('opHoursCalcDescr')
    location.google_calendar_id = location_info.get('googleCalendarId')
    location.online_ordering = location_info.get('onlineOrdering')
    location.online_order_url = location_info.get('onlineOrderUrl')
    location.contact_phone = location_info.get('contactPhone')
    location.contact_email = location_info.get('contactEmail')
    location.service_unit_id = location_info.get('serviceUnitId')
    location.campus_area = location_info['campusArea'].get('descr')
    location.campus_area_short = location_info['campusArea'].get('descrshort')
    location.latitude = location_info.get('latitude')
    location.longitude = location_info.get('longitude')
    location.location_name = location_info.get('location')

    location.save()

    return location

def create_operating_hour(date, location):
    OperatingHour.objects.create(date=date, location=location)