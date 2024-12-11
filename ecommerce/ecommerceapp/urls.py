from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('product/', views.ProductView.as_view(), name='product'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('product/<int:product_id>/', views.ProductDetailView.as_view(), name='detail-product'),
    path('order-success/', views.OrderSuccessView.as_view(), name='order_success'),
    path('update-payment-status/', views.update_payment_status, name='update_payment_status'),
    path('midtrans-payment-handler/', views.midtrans_payment_handler, name='midtrans_payment_handler'),
]