from django.shortcuts import render,redirect
from carts.models import CartItem,Cart
from . models import Order,OrderProduct,Payment
from . forms import OrderForm
# from django.db.models.signals import post_save
# from django.dispatch import receiver
import datetime
from django.shortcuts import render, get_object_or_404
from orders.models import Order,OrderProduct
from django.contrib import messages
# Create your views here.
def place_order(request,total = 0, quantity = 0):
    current_user = request.user
    
    # If the cart count is <= 0 ,then redirect bak to store
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <=0 :
        return redirect('store')
    
    grand_total = 0
    tax =0 
    for cart_item in cart_items:
        total = (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax
    
    if request.method == 'POST':
        form  = OrderForm(request.POST)
        if form.is_valid():
            # store all the billing information inside order table
            data = Order()
            data.user= current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            
            # generate orderid
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number=order_number
              # ... existing code ...
            data.payment_method = 'COD'  # Set payment method to COD
            data.save()
            
            
            order = Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)
            
           
            cart_items = CartItem.objects.filter(user=request.user)

            for item in cart_items:
                order_product = OrderProduct()
                order_product.order_id = order.id
                order_product.user_id = request.user.id
                order_product.product_id = item.product_id
                order_product.quantity = item.quantity
                order_product.product_price = item.product.price
                order_product.ordered = True
                order_product.save()
            
            context ={
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'tax':tax,
                'grand_total':grand_total,
            }
             # Redirect to success page after payment
            # CartItem.objects.filter(user=request.user).delete()
            messages.success(request, 'Order placed successfully!')
            return redirect('order_success')
                

    else:
        return redirect('checkout')
    


# def order_details(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     return render(request, 'greatkart/orders/order_details.html', {'order': order})
    
def payments(request):
    
    # order = Order.objects.all()
    # # Move the cart _items to order_product table
    # cart_items = CartItem.objects.filter(user=request.user)
    # payment = Payment(
    #         user = user
    #         payment_id = payment_id
    #         payment_method = request.payment_method
    #         amount_paid = order.order_total
    #         status =status
            
    # )
    
    # for item in cart_items:
    #     order_products = OrderProduct()
    #     order_products.order_id = order.id
    #     order_products.payment = Payment
    
    
    
    
    return render(request,'greatkart/orders/payments.html')
            
def order_success(request):
    
    # Move the cart _items to order_product table
    # cart_items = CartItem.objects.filter(user=request.user)
    
    # for item in cart_items:
    #     order_products = OrderProduct()
    #     order_products.order_id = order.id
    
    # reduce the sold products
    
    
    # Clear the cart
    
    
    # send  order reciewve email to the customer
    
    # send order number and transacton id back to thabk you page
    
    
    
    
    return render(request,'greatkart/orders/order_success.html')

def cancel_order(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        order.cancelled = True
        order.save()
        for item in order.orderitem_set.all():
            item.cancelled_quantity = item.quantity
            item.save()
            product = item.product
            product.stock += item.quantity
            product.save()
        messages.success(request, 'Order cancelled successfully!')
        return redirect('orders_management')
    return render(request, 'myadmin/cancel_order.html', {'order': order})

def cancel_order_item(request, order_id, item_id):
    order = Order.objects.get(id=order_id)
    item = OrderProduct.objects.get(id=item_id)
    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        item.cancelled_quantity = item.quantity
        item.save()
        product = item.product
        product.stock += item.quantity
        product.save()
        messages.success(request, 'Order item cancelled successfully!')
        return redirect('orders_management')
    return render(request, 'myadmin/cancel_order_item.html', {'order': order, 'item': item})