from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order,name='place_order'),
    path('payments/', views.payments,name='payments'),
    path('order_success/',views.order_success,name='order_success'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('cancel_order_item/<int:order_id>/<int:item_id>/', views.cancel_order_item, name='cancel_order_item'),
    # path('orders/order_details/<int:order_id>/', views.order_details, name='order_details'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)