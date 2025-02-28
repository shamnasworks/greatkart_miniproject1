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

# Create your views here.
def index(request):
    
    return render(request,'myadmin/admin_panel.html')



# user management

def user_management(request):
    users=Account.objects.all().order_by('-id')
    # paginator = Paginator(users,1)
    # page = request.GET.get('page')
    # paged_user=paginator.get_page(page)
    # user_count = users.count()
    if request.method == 'POST':            
        search = request.POST['search']         
        searchresult = Account.objects.filter(username__contains=search)           
        return render(request,'myadmin/search.html',{'result':searchresult})          
    # paginator = Paginator(users,3)
    # page = request.GET.get('page')
    # paged_product=paginator.get_page(page)       
   
    dict_user={
            'users':users,
            
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
    if request.method == 'POST':            
        search = request.POST['search']         
        searchresult = Category.objects.filter(category_name__contains=search)           
        return render(request,'myadmin/search_category.html',{'result':searchresult})          
                

    dict_category = {
        'categories': categories,
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

    dict_product = {
        'products': products,
    }

    return render(request, 'myadmin/product_management.html', dict_product)



def product_edit(request, product_id):
    product_name=request.POST['product_name']
    slug=request.POST['slug']
    description=request.POST['description']
    price=request.POST['price']
    images = request.FILES['images']
    stock=request.POST['stock']
    is_avialble=request.POST['is_available']
    category =request.POST['category']
    updated_product= Product.objects.filter(id=product_id)
    updated_product.update(product_name=product_name,slug=slug)

    if Product.objects.filter(product_name__contains=product_name).exists():
        return redirect(product_management)
    else:
        updated_product.update(product_name=product_name,slug=slug)
        return redirect(product_management)
  

def product_remove(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('product_management')
   
   
def add_product(request):
    if request.method == 'POST':
        product_name = request.POST['productname']
        slug = request.POST['slug']
        description = request.POST['description']
        product_images = request.FILES.get('images')
        stock=request.POST['stock']
        is_avialble=request.POST['is_available']
        category =request.POST['category']
        
        product = Product()

       
        product.product_name = product_name
        product.slug = slug
        product.description = description
        product.images = product_images
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