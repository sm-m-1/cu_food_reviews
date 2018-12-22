import re

from django import forms
from django.forms import ModelForm

from meal_reviews.models import Review
from .bad_words import BAD_WORDS

class ReviewForm(ModelForm):

    class Meta:
        model = Review
        fields = [
            'rating',
            'comment',
        ]

    def clean(self):
        data = super().clean()
        return data

    def clean_comment(self):
        comment = self.cleaned_data.get("comment")
        sentence_list = re.findall("[a-zA-Z0-9',.?!]+", comment)
        for word in sentence_list:
            if word.lower() in BAD_WORDS: raise forms.ValidationError("Please try to use more formal words.")
        return comment





