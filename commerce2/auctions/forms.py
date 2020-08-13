from django import forms
from django.forms import ModelForm
from auctions.models import Product, Comments

class ProductForm(forms.ModelForm):
    class Meta:
        model= Product
        fields= ["title", "description", "price", "image", "category"]
        #fields= ["title", "description", "price",  "category"]

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comments
        fields=["comment"]