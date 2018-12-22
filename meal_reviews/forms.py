import re

from django import forms

from .bad_words import BAD_WORDS

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

    def clean_comment(self):
        comment = self.cleaned_data.get("comment")
        sentence_list = re.findall("[a-zA-Z0-9',.?!]+", comment)
        for word in sentence_list:
            if word.lower() in BAD_WORDS: raise forms.ValidationError("Please try to use more formal words.")
        return comment





