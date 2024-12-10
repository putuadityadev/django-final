from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('product/', views.ProductView.as_view(), name='product'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('product/<int:product_id>/', views.ProductDetailView.as_view(), name='detail-product'),
]