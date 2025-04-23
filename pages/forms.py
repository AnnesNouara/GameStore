from django import forms
from .models import Rental, Review

class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['duration']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating','comment']
        widgets = { 'comment': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Leave a comment'})}


