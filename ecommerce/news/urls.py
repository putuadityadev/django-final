from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_news, name='create_news'),
    path('', views.news, name='news'),
]