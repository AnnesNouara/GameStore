from django import forms
from .models import Rental 

class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['duration'] 

