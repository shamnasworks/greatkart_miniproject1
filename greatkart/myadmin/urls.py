from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    # path('', views.myadmin,name='myadmin'),
    path('', views.index, name="admin_dashboard"),
    path('admin/', views.adminn, name="adminn"),
    # path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    
    path('register/<int:verify>/', views.register, name='register'),
    path('delete_record/<int:user_id>/', views.delete_record, name='delete'),
    path('update_record/<int:user_id>/', views.update_record, name='update'),
    path('user_management/', views.user_management,name='user_management'),
    path('admin/block/<int:user_id>/', views.block_user, name='block_user'),
    path('admin/unblock/<int:user_id>/', views.unblock_user, name='unblock_user'),
    
    
    path('product_management/', views.product_management,name='product_management'),
    path('product/edit/<int:product_id>/', views.product_edit, name='product_edit'),
    path('product/remove/<int:product_id>/', views.product_remove, name='product_remove'),
    path('category_management/', views.category_management,name='category_management'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)