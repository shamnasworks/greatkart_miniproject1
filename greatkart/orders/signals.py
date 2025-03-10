# orders/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from carts.models import CartItem

@receiver(post_save, sender=Order)
def delete_cart_items(sender, instance, created, **kwargs):
    if created:
        CartItem.objects.filter(user=instance.user).delete()
        cart_item=CartItem.objects.all()
        print(cart_item)
        