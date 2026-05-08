from django import forms
from .models import Listing, CATEGORY_CHOICES


class ListingForm(forms.ModelForm):
    class Meta:
        model  = Listing
        fields = ['title', 'price', 'category', 'description', 'image1', 'image2', 'image3']

    def clean_description(self):
        desc = self.cleaned_data.get('description', '')
        if len(desc.strip()) < 10:
            raise forms.ValidationError('Description must be at least 10 characters.')
        return desc

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError('Price cannot be negative.')
        return price
