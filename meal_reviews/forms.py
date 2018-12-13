from django import forms
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from meal_items.models import MealItem
from meal_reviews.models import Review

class ReviewForm(forms.Form):
    star_rating = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                'id': "input-1",
                'name': "input-1",
                'class': "rating rating-loading",
                'data-min': "0",
                'data-max': "5",
                'data-step': "1"
            }
        ),
        required=True
    )
    comment = forms.CharField(
        label="comments",
        widget=forms.Textarea(
            attrs={
                'class': 'form-control my-2',
                'data-size': "sm",
                'id' : "review_comment",
                'name' : "review_comment",
                'rows' : '3'
            }
        ),
        required=False,
    )

class ReviewPost(SingleObjectMixin, FormView):
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