from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('control/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('rest/', include('client.urls')),
    path('vendor/', include('vendor.urls')),
    path('user/', include('users.urls')),
    path('admin/', include('adminn.urls')),
    path('delivery/', include('delivery.urls')),
]
