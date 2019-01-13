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

