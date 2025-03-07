from django.http import HttpResponse
from django.shortcuts import render
from store.models import Product
from django.contrib.sites.models import Site

site = Site.objects.get(id=1)

def home(request):
    products = Product.objects.all().filter(is_available=True)
    
    context = {
        'products':products,
    }
    
    return render(request,'greatkart/home.html',context)