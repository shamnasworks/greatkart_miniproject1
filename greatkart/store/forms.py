# forms.py
from django import forms
from .models import ProductGallery

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductGallery
        fields = ('image',)