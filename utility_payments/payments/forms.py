from django import forms
from .models import Tariff

class TariffForm(forms.ModelForm):
    class Meta:
        model = Tariff
        fields = ['electricity', 'gas', 'water']