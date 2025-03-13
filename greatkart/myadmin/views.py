from django.shortcuts import render,redirect
from  accounts.models import Account,MyAccountManager
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import auth
from accounts.views import userlogin,register
from django.contrib import messages
from store.models import Product,Variation
from category.models import Category
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from accounts.views import dashboard
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from orders.models import Order,OrderProduct,OrderStatusHistory
# Create your views here.
def index(request):
    
    return render(request,'myadmin/admin_panel.html')



# user management

def user_management(request):
    users=Account.objects.all().order_by('-id')
    paginator = Paginator(users,1)
    page = request.GET.get('page')
    paged_user=paginator.get_page(page)
    
    start_index = paginator.per_page * (paged_user.number - 1) + 1
    end_index = start_index + paginator.per_page - 1

    if end_index > paginator.count:
        end_index = paginator.count
    
    
    
    
    user_count = users.count()
    if request.method == 'POST':            
        search = request.POST['search']         
        searchresult = Account.objects.filter(username__contains=search)           
        return render(request,'myadmin/search.html',{'result':searchresult})          
    # paginator = Paginator(users,3)
    # page = request.GET.get('page')
    # paged_product=paginator.get_page(page)       
   
    dict_user={
            'users':paged_user,
                 'start_index': start_index,
    'end_index': end_index,
            
        }
    return render(request,'myadmin/user_management.html',dict_user)

def block_user(request, user_id):
    user = Account.objects.get(id=user_id)
    user.is_active = False
    user.save()
    return redirect('user_management')

def unblock_user(request, user_id):
    user = Account.objects.get(id=user_id)
    user.is_active = True
    user.save()
    return redirect('user_management')



# category
def category_management(request):
    categories = Category.objects.filter().order_by('-id')
    
    paginator = Paginator(categories,1)
    page = request.GET.get('page')
    paged_category=paginator.get_page(page)
    user_count = categories.count()
    
    start_index = paginator.per_page * (paged_category.number - 1) + 1
    end_index = start_index + paginator.per_page - 1

    if end_index > paginator.count:
        end_index = paginator.count
    
    if request.method == 'POST':            
        search = request.POST['search']         
        searchresult = Category.objects.filter(category_name__contains=search)           
        return render(request,'myadmin/search_category.html',{'result':searchresult})          
                

    dict_category = {
        'categories': paged_category,
             'start_index': start_index,
    'end_index': end_index,
    }

    return render(request, 'myadmin/category_management.html', dict_category)



def category_edit(request, category_id):
    category_name=request.POST['category_name']
    slug=request.POST['slug']
    updated_category = Category.objects.filter(id=category_id)
    updated_category.update(category_name=category_name,slug=slug)

    if Category.objects.filter(category_name__contains=category_name).exists():
        return redirect(category_management)
    else:
        updated_category.update(category_name=category_name,slug=slug)
        return redirect(category_management)

def category_delete(request,category_id):
    del_record = Category.objects.filter(id=category_id)
    del_record.delete()
    return redirect(category_management)


def category_add(request):
    if request.method == 'POST':
        category_name = request.POST['category_name']
        slug = request.POST['slug']
        description = request.POST['description']
        cart_image = request.FILES['cart_image']

        category = Category()
        category.category_name = category_name
        category.slug = slug
        category.description = description
        category.cart_image = cart_image
        category.save()

        return redirect('category_management')
   





# product management
  
def product_management(request):
    products = Product.objects.filter(is_available=True)
    if request.method == 'POST':            
        search = request.POST['search']         
        searchresult = Product.objects.filter(product_name__contains=search)           
        return render(request,'myadmin/product_search.html',{'result':searchresult})     
    paginator = Paginator(products,1)
    page = request.GET.get('page')
    paged_products=paginator.get_page(page)
    prodcuct_count = products.count()
    
    
    start_index = paginator.per_page * (paged_products.number - 1) + 1
    end_index = start_index + paginator.per_page - 1

    if end_index > paginator.count:
        end_index = paginator.count


    dict_product = {
        'products': products,
                  'start_index': start_index,
    'end_index': end_index,
    }

    return render(request, 'myadmin/product_management.html', dict_product)




def product_edit(request, product_id):
    product = Product.objects.get(id=product_id)
    
    if request.method == 'POST':
        product_name = request.POST['product_name']
        slug = request.POST['slug']
        description = request.POST['description']
        price = request.POST['price']
        stock = request.POST['stock']
        is_available = request.POST.get('is_available', False)
        category = request.POST['category']
        
        # Validation
        if not product_name:
            messages.error(request, 'Product name is required.')
            return render(request, 'product_edit.html', {'product': product})
        
        if not slug:
            messages.error(request, 'Slug is required.')
            return render(request, 'product_edit.html', {'product': product})
        
        if not description:
            messages.error(request, 'Description is required.')
            return render(request, 'product_edit.html', {'product': product})
        
        if not price:
            messages.error(request, 'Price is required.')
            return render(request, 'product_edit.html', {'product': product})
        
        if not stock:
            messages.error(request, 'Stock is required.')
            return render(request, 'product_edit.html', {'product': product})
        
        if not category:
            messages.error(request, 'Category is required.')
            return render(request, 'product_edit.html', {'product': product})
        
        # Check if product name already exists
        if Product.objects.filter(product_name__iexact=product_name).exclude(id=product_id).exists():
            messages.error(request, 'Product name already exists.')
            return render(request, 'product_edit.html', {'product': product})
        
        # Update product
        product.product_name = product_name
        product.slug = slug
        product.description = description
        product.price = price
        product.stock = stock
        product.is_available = is_available
        product.category = category
        
        # Handle image upload
        if 'images' in request.FILES:
            product.images = request.FILES['images']
        
        product.save()
        
        messages.success(request, 'Product updated successfully.')
        return redirect('product_management')
    
    return render(request, 'product_edit.html', {'product': product})

def product_remove(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('product_management')
   
   
def add_product(request):
    if request.method == 'POST':
        # product_name = request.POST.get('productname')
        product_name = request.POST['productname']
        slug = request.POST['slug']
        description = request.POST['description']
        product_images = request.FILES.get('images')
        stock=request.POST['stock']
        is_available = request.POST.get('is_available', False)
        category =request.POST['category']
        
        product = Product()

       
        product.product_name = product_name
        product.slug = slug
        product.description = description
        product.images = product_images
        product.is_available=is_available
        product.stock=stock
        product.category=category
        product.save()

        return redirect('product_management')
   









@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def register(request,verify):
    if request.method == 'POST':
        if request.POST['username']!='':
            email = request.POST['email']
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            password = request.POST['password']
            confirmpass = request.POST['confirmpass']
            if password == confirmpass:
                if Account.objects.filter(username=username).exists():
                    messages.info(request,'Username is already eixst')
                    return redirect(register,1)
                else:
                    user = Account.objects.create_user(email=email,username=username,first_name=first_name,last_name=last_name,password=password)
                    user.save()
                    if verify==1:
                        return redirect(user_management)
                return redirect(index)
            else:
                messages.info(request,'Password do not match')
                return redirect(register,0)
        else:
            messages.info(request,'some field is empty')
            return redirect(register,0)
    else:
        return render(request,'greatkart/accounts/register.html')


# @cache_control(no_cache=True,must_revalidate=True,no_store=True)            
@login_required(login_url='/userlogin')      
def adminn(request):           
    if not request.user.is_admin:           
        return redirect(index)           
    
    else:           
        dict_user={
            'users':Account.objects.all().order_by('id')
        }
        return render(request,'myadmin/admin_panel.html',dict_user)
    
    
# @cache_control(no_cache=True,must_revalidate=True,no_store=True)            
# @login_required(login_url='/login') 
def logout(request):
    auth.logout(request)            
    return redirect(userlogin) 


def delete_record(request,user_id):
    del_record = Account.objects.filter(id=user_id)
    del_record.delete()
    return redirect(user_management)



def update_record(request,user_id):
    username=request.POST['username']
    email=request.POST['email']
    update_user = Account.objects.filter(id=user_id)
    update_user.update(username=username,email=email)

    if Account.objects.filter(username__contains=username).exists():
        return redirect(user_management)
    else:
        update_user.update(username=username,email=email)
        return redirect(user_management)
    

# views.py
def update_order_status(request, order_id):
    order = Order.objects.get(id=order_id)
    new_status = request.POST['status']

    # Define the allowed status transitions
    allowed_transitions = {
        'New': ['Accepted', 'Cancelled'],
        'Accepted': ['Completed', 'Cancelled'],
        'Completed': [],
        'Cancelled': []
    }

    # Check if the new status is in the allowed transitions
    if new_status in allowed_transitions.get(order.status, []):
        order.status = new_status
        order.save()

        # Create a new OrderStatusHistory object
        OrderStatusHistory.objects.create(order=order, old_status=order.status, new_status=new_status)

        messages.success(request, 'Order status updated successfully!')
    else:
        messages.error(request, 'Invalid status transition!')

    return redirect('orders_management')




def orders_management(request):
    orders = Order.objects.all().order_by('-id')
    # if request.method == 'POST':
    #     order_id = request.POST['order_id']
    #     new_status = request.POST['new_status']

    #     order = Order.objects.get(id=order_id)

    #     if is_valid_next_status(order, new_status):
    #         old_status = order.status
    #         order.status = new_status
    #         order.save()

    #         OrderStatusHistory.objects.create(order=order, old_status=old_status, new_status=new_status)

    #         messages.success(request, 'Order status updated successfully!')
    #     else:
    #         messages.error(request, 'Invalid status transition!')

    paginator = Paginator(orders, 3)
    page = request.GET.get('page')
    paged_orders = paginator.get_page(page)
    
    start_index = paginator.per_page * (paged_orders.number - 1) + 1
    end_index = start_index + paginator.per_page - 1

    if end_index > paginator.count:
        end_index = paginator.count

    dict_orders = {
        'orders': paged_orders,
         'start_index': start_index,
    'end_index': end_index,
    }
    return render(request, 'myadmin/orders_management.html', dict_orders)


# def is_valid_next_status(order, new_status):
#     current_status = order.status
#     status_history = OrderStatusHistory.objects.filter(order=order).order_by('-timestamp')

#     if new_status == current_status:
#         return False

#     valid_transitions = {
#         'pending': ['accepted', 'rejected'],
#         'accepted': ['shipped', 'cancelled'],
#         'shipped': ['delivered'],
#         'rejected': [],
#         'cancelled': [],
#         'delivered': [],
#     }

#     if new_status not in valid_transitions.get(current_status, []):
#         return False

#     for history in status_history:
#         if history.new_status == new_status:
#             return False

#     return True