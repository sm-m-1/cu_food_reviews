from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView
from .models import MealItem
from meal_reviews.models import Review
from meal_reviews.forms import ReviewForm, ReviewPost
from django.db.models import Avg

# Create your views here.
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
        view = ReviewPost.as_view()
        return view(request, *args, **kwargs)






