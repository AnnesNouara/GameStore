from django import forms
from .models import Rental  # or whatever your model is

class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['duration']  # or your fields

