from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *

urlpatterns = [
    path("cart", CartApi.as_view(), name="cart"),
    path("wishlist", WishList.as_view(), name="wishlist"),
    path("order", OrderApi.as_view(), name="orders"),
    path("address", AddressApi.as_view(), name="address"),
    path("address/<int:pk>", AddressUpdateApi.as_view(), name="address_id"),
    path("order/<int:pk>", UpdateStatus.as_view(), name="update_status"),
]
