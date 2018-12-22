from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin

from meal_items.models import MealItem
from .forms import AlertForm
from .models import Alert

class MealItemAlertFormView(SingleObjectMixin, FormView):
    template_name = 'meal-item-alert-form.html'
    slug_url_kwarg = 'item_slug'
    form_class = AlertForm
    model = MealItem

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated: return HttpResponseForbidden()
        already_set = Alert.objects.filter(user=request.user, meal_item=self.object).exists()
        if already_set: return HttpResponse("You've already set alert for this item.")
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        new_alert = form.save(commit=False)
        new_alert.meal_item = self.object
        new_alert.user = self.request.user
        new_alert.save()
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('meal_item_alert_success')

def meal_item_alert_success(request):
    return render(request, template_name='meal-item-alert-success.html')