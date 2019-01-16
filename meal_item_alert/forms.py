from django.forms import ModelForm
from django import forms
from .models import Alert

class AlertForm(ModelForm):
    active = forms.BooleanField(required=True)

    class Meta:
        model = Alert
        fields = [
            'active',
        ]

    def clean(self):
        data = super().clean()
        return data