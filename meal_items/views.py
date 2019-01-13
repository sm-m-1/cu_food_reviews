from django.db.models import Avg
from django.urls import reverse
from django.views.generic import DetailView

from meal_reviews.models import Review
from .models import MealItem


class MealItemDetailView(DetailView):
    # model = MealItem
    queryset = MealItem.objects.all()
    template_name = 'meal-item-detail.html'
    slug_url_kwarg = 'item_slug'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        reviews = Review.objects.filter(meal_item_id=self.object)
        context['reviews_list'] = reviews.order_by("-created_on")
        context['create_review_url'] = reverse('meal_item_review', kwargs={'item_slug': self.object.slug})
        context['create_alert_url'] = reverse('meal_item_alert', kwargs={'item_slug': self.object.slug})
        context['average_rating'] = Review.objects.filter(meal_item_id=self.object.id).aggregate(Avg('rating')).get('rating__avg')

        return context



