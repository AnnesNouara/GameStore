from django import forms
from pages.models import Product


class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['stock']