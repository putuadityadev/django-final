from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ecommerceapp.urls')),
    path('auth/', include('authcart.urls')),
    path('news/', include('news.urls')),
    path('profile/', include('myprofile.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)


