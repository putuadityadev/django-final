from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_profile, name='view_profile'),
    path('edit_profile/', views.editprofile, name='edit_profile'),
    path('favorite/<int:product_id>/', views.toggle_favorite, name='toggle_favorite'),
]