from django.urls import path
from authcart import views

urlpatterns = [
  path('signup/', views.signup, name='signup'),
  path('login/', views.handle_login, name='handlelogin'),
  path('logout/', views.handle_logout, name='handlelogout'),
  path('activate/<uidb64>/<token>', views.ActivateAccountView.as_view(), name='activate')
]
