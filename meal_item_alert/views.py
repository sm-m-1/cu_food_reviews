from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import FormView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse_lazy

from meal_items.models import MealItem
from .forms import AlertForm
from .models import Alert, user_did_not_create_alert_for_item


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_did_not_create_alert'] = user_did_not_create_alert_for_item(self.request.user, self.object)
        return context


class MealItemAlertDeleteView(DeleteView):
    model = Alert
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('meal_items_alert_list')
    template_name = 'alert_confirm_delete.html'
    # def get_object(self, queryset=None):
    #     id_ = self.kwargs.get('id')
    #     return super().get_object(queryset)


def meal_item_alert_success(request):
    return render(request, template_name='meal-item-alert-success.html')