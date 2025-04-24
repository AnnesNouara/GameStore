from django import forms
from .models import Rental, Review

class RentalForm(forms.ModelForm):
    duration = forms.IntegerField(
    min_value=1,
    max_value=30,
    label='Rental Duration (days)',
    help_text='Choose how many days you want to rent this product for.')
     
    class Meta:
        model = Rental
        fields = ['duration']


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, i) for i in range(1, 6)], #This is makes the choices be 1-5
        label='Rating',
        help_text='Rate from 1 (worst) to 5 (best)',
        widget=forms.Select()
    )
    
    class Meta:
        model = Review
        fields = ['rating','comment']
        widgets = { 'comment': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Leave a comment'})}


