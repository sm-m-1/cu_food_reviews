from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, FormView, DeleteView, UpdateView
from django.views.generic.detail import SingleObjectMixin

from .models import MealItem
from meal_reviews.models import Review
from meal_reviews.forms import ReviewForm


class ReviewFormView(SingleObjectMixin, FormView):
    template_name = 'meal-item-review-form.html'
    slug_url_kwarg = 'item_slug'
    form_class = ReviewForm
    model = MealItem

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        logged_in = request.user.is_authenticated
        if not logged_in: return HttpResponseForbidden()

        already_reviewed = Review.objects.filter(user=request.user, menu_item=self.object).exists()
        if already_reviewed: return HttpResponse("You've already reviewed this item. You can edit it in My Accounts section.")

        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        new_review = form.save(commit=False)
        new_review.menu_item_id = self.object.id
        new_review.user = self.request.user
        new_review.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('meal_item_review_success')

def meal_item_review_success(request):
    return render(request, template_name='meal-item-review-success.html')


class ReviewDeleteView(DeleteView):
    model = Review
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('meal_reviews_list')
    template_name = 'review_confirm_delete.html'


class ReviewUpdateView(UpdateView):
    model = Review
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('meal_reviews_list')
    template_name = 'review_update_form.html'
    # fields = ['rating', 'comment']
    form_class = ReviewForm
