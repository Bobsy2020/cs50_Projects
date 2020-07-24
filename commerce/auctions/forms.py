from django import forms
from django.forms import ModelForm
from auctions.models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model= Listing
        fields= ["title", "description", "price", "image", "category"]
        #fields= ["title", "description", "price",  "category"]