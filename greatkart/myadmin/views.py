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


def user_management(request):
    users=Account.objects.all().order_by('-id')
    paginator = Paginator(users,1)
    page = request.GET.get('page')
    paged_user=paginator.get_page(page)
    user_count = users.count()
  
   
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








   
def product_management(request):
    products = Product.objects.filter(is_available=True)

    dict_product = {
        'products': products,
    }

    return render(request, 'myadmin/product_management.html', dict_product)



def product_edit(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_management')
    else:
        form = ProductForm(instance=product)
    return render(request, 'myadmin/product_edit.html', {'form': form})

def product_remove(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('product_management')
    return render(request, 'myadmin/product_remove.html', {'product': product})

def category_management(request):
    products = Product.objects.filter(is_available=True)

    dict_product = {
        'products': products,
    }

    return render(request, 'myadmin/category_management.html', dict_product)




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
    if request.method == 'POST':            
        search = request.POST['search']         
        searchresult = Account.objects.filter(username__contains=search)           
        return render(request,'search.html',{'result':searchresult})          
                
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