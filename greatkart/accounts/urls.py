from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('register', views.register,name='register'),
    path('userlogin', views.userlogin,name='userlogin'),
    path('userlogout',views.userlogout,name='userlogout'),
    path('actiavte/<uidb64>/<token>/',views.activate,name='activate'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('',views.dashboard,name='dashboard'),
    path('forgotpassword/',views.forgotpassword,name='forgotpassword'),
    path('resetpassword/',views.resetpassword,name='resetpassword'),
    path('resetpassword_validate/<uidb64>/<token>/',views.resetpassword_validate,name='resetpassword_validate'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('verify_email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('change_password/',views.change_password,name='change_password'),
    path('my_orders/',views.my_orders,name='my_orders'),
    path('addresses/', views.address_list, name='address_list'),
    path('addresses/add/', views.address_add, name='address_add'),
    path('addresses/<pk>/update/', views.address_update, name='address_update'),
    path('addresses/<pk>/delete/', views.address_delete, name='address_delete'),



]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)