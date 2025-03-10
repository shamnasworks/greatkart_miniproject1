from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order,name='place_order'),
    path('payments/', views.payments,name='payments'),
    path('order_success/',views.order_success,name='order_success'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)