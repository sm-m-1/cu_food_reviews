from django.http import HttpResponse, HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, FormView
from django.views.generic.detail import SingleObjectMixin

from .models import MealItem
from meal_reviews.models import Review
from meal_reviews.forms import ReviewForm
from django.db.models import Avg


class ReviewFormView(SingleObjectMixin, FormView):
    template_name = 'meal-item-review-form.html'
    slug_url_kwarg = 'item_slug'
    form_class = ReviewForm
    model = MealItem

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        logged_in = request.user.is_authenticated
        if not logged_in: return HttpResponseForbidden()

        already_reviewed = Review.objects.filter(author=request.user, menu_item=self.object).exists()
        if already_reviewed: return HttpResponse("You've already reviewed this item.")

        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        data = form.cleaned_data
        Review.objects.create(
            rating=data.get('star_rating', 4),
            comment=data.get('comment', ''),
            menu_item_id=self.object.id,
            author=self.request.user
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('meal_item_review_success')

def meal_item_review_success(request):
    return render(request, template_name='meal-item-review-success.html')


class MealItemDetailView(DetailView):
    # model = MealItem
    queryset = MealItem.objects.all()
    template_name = 'meal-item-detail.html'
    slug_url_kwarg = 'item_slug'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        # context['review_form'] = ReviewForm()
        # already_reviewed = self.request.session.get(self.object.slug)
        # if not self.request.user.is_authenticated:
        #     context['hide_review_form'] = True
        # else:
        #     already_reviewed = Review.objects.filter(author=self.request.user, menu_item=self.object).exists()
        #     context['hide_review_form'] = already_reviewed
        reviews = Review.objects.filter(menu_item_id=self.object)
        context['reviews_list'] = reviews.order_by("-created_on")
        context['create_review_url'] = reverse('meal_item_review', kwargs={'item_slug': self.object.slug})
        context['average_rating'] = Review.objects.filter(menu_item_id=self.object.id).aggregate(Avg('rating')).get('rating__avg')
        print("context: ", context)
        return context



