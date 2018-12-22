from django.forms import ModelForm
from .models import Alert

class AlertForm(ModelForm):

    class Meta:
        model = Alert
        fields = [
            'active',
        ]

    def clean(self):
        data = super().clean()
        return data