from django.core.management.base import BaseCommand, CommandError

from django.core.management.base import BaseCommand, CommandError
import json
import urllib.request

API_ENDPOINT_URL = "https://now.dining.cornell.edu/api/1.0/dining/eateries.json"


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        response = load_data_from_api_endpoint(API_ENDPOINT_URL)
        data = response.get('data')

        print("items: ", len(response["data"]["eateries"]))

        pass

def load_data_from_api_endpoint(api_url):
    page = urllib.request
    contents = json.load(urllib.request.urlopen(api_url))
    return contents