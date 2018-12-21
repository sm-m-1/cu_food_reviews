from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, FormView
from django.views.generic.detail import SingleObjectMixin

from .models import MealItem
from meal_reviews.models import Review
from meal_reviews.forms import ReviewForm
from django.db.models import Avg


class ReviewFormPostView(SingleObjectMixin, FormView):
    template_name = 'meal-item-detail.html'
    slug_url_kwarg = 'item_slug'
    form_class = ReviewForm
    model = MealItem

    def post(self, request, *args, **kwargs):
        # if not request.user.is_authenticated:
        #     return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        data = form.data
        Review.objects.create(
            rating=data.get('star_rating', 4),
            comment=data.get('comment', ''),
            menu_item_id=self.object.id
        )
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('meal_item', kwargs={'item_slug': self.object.slug})


class MealItemDisplay(DetailView):
    # model = MealItem
    queryset = MealItem.objects.all()
    template_name = 'meal-item-detail.html'
    slug_url_kwarg = 'item_slug'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['form'] = ReviewForm()
        reviews = Review.objects.filter(menu_item_id=self.object)
        context['reviews_list'] = reviews.order_by("-created_on")
        context['average_rating'] = Review.objects.filter(menu_item_id=self.object.id).aggregate(Avg('rating')).get('rating__avg')
        print("context: ", context)
        return context

class MealItemDetail(View):
    def get(self, request, *args, **kwargs):
        view = MealItemDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ReviewFormPostView.as_view()
        return view(request, *args, **kwargs)



