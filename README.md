# This is a web application built with the data from Cornell Dining.

Users can view the menu list for all Cornell locations for the next 7 days. 

Users can view and write reviews for menu items. 

Users can set up email alerts for items at any Cornell dining location.

The web app is currently deployed at a DigitalOcean Ubuntu Droplet.  
The current version can be viewed at:  
https://www.cornellfood.me/

This web app is built with Python, Django, PostgreSQL, Celery, RabbitMQ, 
MailGun, and Bootstrap.

The menu data is consumed from this Cornell Dining API:  
https://now.dining.cornell.edu/api/1.0/dining/eateries.json

This is the Cornell menu website that is built from from the API. It only allows 
you to view menu items.  
https://now.dining.cornell.edu/eateries

The menu data is consumed from the Cornell Dining API as is and similar models are created  
in the Django database.

The ['/locations'](locations/views.py) view endpoint required the most work.   


In this view I de-structure the saved Models  
from the Django database given a date and a campus region.  

The data structure looks like this before passing it to the template for rendering:  

```
data = [
  {
    'location': location1,
    'location_data': [
      {
        'event': Lunch,
        'meal_category_data': [
            {
              'category': Soup Station,
              'category_items': [
                  vegetable soup, chicken soup, ......
              ]
            },
          	{
              'category': Salad Bar Station,
              'category_items': [
                  Salad1, Salad2, ......
              ]
            },
         ]
      },
      {
        'event': Diner,
        'meal_category_data': [
            {
              'category': Soup Station,
              'category_items': [
                  vegetable soup, chicken soup, ......
              ]
            },
            {
              'category': Salad Bar Station,
              'category_items': [
                  Salad1, Salad2, ......
              ]
            },
         ]
      },
      .....
    ]
  },
  {
    'location': location2,
    'location_data': [
      {
        'event': Lunch,
        'meal_category_data': [
            {
              'category': Soup Station,
              'category_items': [
                  vegetable soup, chicken soup, ......
              ]
            },
            {
              'category': Salad Bar Station,
              'category_items': [
                  Salad1, Salad2, ......
              ]
            },
         ]
      },
      {
        'event': Diner,
        'meal_category_data': [
            {
              'category': Soup Station,
              'category_items': [
                  vegetable soup, chicken soup, ......
              ]
            },
            {
              'category': Salad Bar Station,
              'category_items': [
                  Salad1, Salad2, ......
              ]
            },
         ]
      },
      .....
    ]
  },
  .....
]
```