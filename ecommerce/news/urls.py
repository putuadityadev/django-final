from django.urls import path
from .views import NewsListView, CreateNewsView

urlpatterns = [
    path('create/', CreateNewsView.as_view(), name='create_news'),
    path('', NewsListView.as_view(), name='news'),
]