from __future__ import absolute_import, unicode_literals

from datetime import datetime
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.core.mail import send_mail, EmailMultiAlternatives
from cu_food_reviews.celery import app
from cu_food_reviews import settings
from .models import Alert

@app.task
def celery_send_email(mail_subject, text_content, html_content, from_email, to_email):
    msg = EmailMultiAlternatives(
        mail_subject, text_content, from_email, to_email
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@app.task
def send_users_alert_email():
    unsubscribe_link = reverse_lazy('meal_items_alert_list')
    locations_link = reverse_lazy('location_list')
    domain = settings.DOMAIN_NAME
    today = datetime.now().date()
    date = today.isoformat()
    text_content = ''

    all_alerts = Alert.objects.all()
    for alert in all_alerts:
        user = alert.user
        food_name = "{} at {}".format(alert.meal_item.name, alert.meal_item.meal_location)
        mail_subject = "Cornell Food Alert - " + food_name
        to_email = [user.email]
        html_content = render_to_string('meal-alert-email.html', {
            'user': user,
            'domain': domain,
            'unsubscribe_link': unsubscribe_link,
            'locations_link': locations_link,
            'food_name': food_name,
            'date': date,
        })
        celery_send_email.delay(
            mail_subject,
            text_content, html_content,
            settings.DEFAULT_FROM_EMAIL,
            to_email
        )
