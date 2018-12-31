from __future__ import absolute_import, unicode_literals

from datetime import datetime
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.core.mail import send_mail, EmailMultiAlternatives
from cu_food_reviews.celery import app
from cu_food_reviews import settings

@app.task
def send_users_alert_email():
    user = "test_user@gmail.com"
    food_name = "Chicken at Risley"
    today = datetime.now().date()
    date = today.isoformat()
    mail_subject = "Cornell Food Alert - " + food_name
    unsubscribe_link = reverse_lazy('meal_items_alert_list')
    text_content = ''
    to_email = ['mashthemyth@gmail.com']

    html_content = render_to_string('meal-alert-email.html', {
        'user': user,
        'unsubscribe_link': unsubscribe_link,
        'food_name': food_name,
        'date': date,
    })
    msg = EmailMultiAlternatives(
        mail_subject, text_content, settings.DEFAULT_FROM_EMAIL, to_email
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    # send_mail(
    #     mail_subject,
    #     message,
    #     settings.DEFAULT_FROM_EMAIL,
    #     to_email,
    #     fail_silently=False
    # )