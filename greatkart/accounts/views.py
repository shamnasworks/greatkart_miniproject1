from django.shortcuts import render,redirect
from .forms import RegistrationForm
from .models import Account
from carts.models import Cart,CartItem
from carts.views import _cart_id
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
#verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

import re
# Create your views here.
def register(request):
    if request.method=='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user = Account.objects.create(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_number=phone_number
            user.save()
            
            # user activation
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('greatkart/accounts/account_verification_mail.html',{
                'user':user,
                 'domain':current_site,
                 'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                  'token':default_token_generator.make_token(user),
                 
             })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            
            messages.success(request,'Thank you for registering with us.We have send verification email to your email address.Please verify it.')
            return redirect('userlogin?command=verification&email='+email)
    else:       
         form = RegistrationForm()
    context = {
         'form': form,
     }
    return render(request, 'greatkart/accounts/register.html',context)

def userlogin(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email=email,password=password)
        
        if user is not None :
            try:
                cart =  Cart.objects.get(cart_id = _cart_id(request) )
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    
                    #Getting the product variations by cart 
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))
                        # item.user=user
                        # item.save()
                    #Get the cart items from the user to access his product variation
                    cart_item = CartItem.objects.filter( user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)
                        
                    # product_variation = [1,2,3,4,6]
                    # ex_var_list = [4,6,3,5] 
                    # to get common product variation from product_variation and ex_variationlist
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id(index)
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user=user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user=user
                                item.save()
            except:
                pass
            auth.login(request,user)
            messages.success(request,'You are now logged in')
            
            if user.is_admin:
                return redirect('admin_dashboard')
            else:
                return redirect('dashboard')
        else:
            messages.error(request,'Invalid login credentials')
            return redirect('userlogin')
    
    return render(request,'greatkart/accounts/userlogin.html')

@login_required(login_url='userlogin')
def userlogout(request):
    auth.logout(request)
    messages.success(request,'You are logged out')
    return redirect('userlogin')


    
def activate(request,uidb64,token):
    try:
        
        uid =  urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,'Congragulations! Your account is activated.')
        return redirect('userlogin')
    else:
        messages.error(request,'Invalid activation link.')
    return redirect('register')


# @login_required(login_url= 'userlogin')
def dashboard(request):
    # orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    # orders_count = orders.count()

    # userprofile = UserProfile.objects.get(user_id=request.user.id)
    # context = {
    #     'orders_count': orders_count,
    #     'userprofile': userprofile,
    # }
    return render(request,'greatkart/accounts/dashboard.html')

def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            
            
            # reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('greatkart/accounts/reset_password_email.html',{
               'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                 'token':default_token_generator.make_token(user),
                 
             })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            
            messages.success(request,'Password reset email has been sent to your email address.')
            return redirect('userlogin')
        else:
            messages.error(request,'Account does not exist')
            return redirect('forgotpassword')
    return render(request,'greatkart/accounts/forgotpassword.html')


def resetpassword_validate(request,uidb64,token):
    try:
        
        uid =  urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        
        user = None
    
    if user is not None and default_token_generator.check_token(user,token):
        
        request.session['uid']=uid
        messages.success(request,'Please reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request,'This link is has been expired.')
        return redirect('userlogin')
def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user= Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password reset successful')
            return redirect('userlogin')
            
        else:
            messages.error(request,'Password do not match')
            return redirect('resetpassword')
    else:
        return render(request,'greatkart/accounts/resetpassword.html')