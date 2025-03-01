from django.db import models
from store.models import Product,ProductGallery
from store.models import Variation
from  accounts.models import Account

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateField(auto_now_add=True)
    
    
    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation,blank=True)
    cart = models.ForeignKey(Cart,models.CASCADE,null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE,default=1)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    def sub_total(self):
        return self.product.price * self.quantity
    
    def __unicode__(self):
        return self.product
    
    
    
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=50, choices=[('percentage', 'Percentage'), ('amount', 'Amount')])
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_discount_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)