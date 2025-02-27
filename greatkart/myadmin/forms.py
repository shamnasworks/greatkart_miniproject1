from django import forms
from store.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('product_name', 'description', 'price', 'images', 'stock', 'is_available', 'category')