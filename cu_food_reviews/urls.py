"""cu_food_reviews URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.contrib.auth import views as auth_views
# auth_views.PasswordResetView
# auth_views.PasswordResetForm
# auth_views.PasswordResetConfirmView
# auth_views.PasswordResetCompleteView
# auth_views.PasswordResetDoneView

from locations.views import LocationList
from meal_items.views import MealItemDetail
from accounts.views import (
    LoginFormView,
    SignUpFormView,
    LogoutFormView,
    signup_success,
    contact_page_success,
    UserActivationView,
    ContactFormView
)

from home.views import HomePageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('locations/', LocationList.as_view(), name='location_list'),
    path('contact/', ContactFormView.as_view(), name='contact_page'),
    path('contact/success', contact_page_success, name='contact_page_success'),
    path('home/items/<slug:item_slug>', MealItemDetail.as_view(), name='meal_item'),

    path('accounts/signup', SignUpFormView.as_view(), name='signup'),
    path('accounts/login', LoginFormView.as_view(), name='login'),
    path('accounts/logout', LogoutFormView.as_view(), name='logout'),
    path('accounts/signup/success', signup_success, name='signup_success'),
    path('accounts/signup/activate/', UserActivationView.as_view(), name='user_activate'),


    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]