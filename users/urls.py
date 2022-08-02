from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *

urlpatterns = [
    path("cart", CartApi.as_view(), name="cart"),
    path("wishlist", WishList.as_view(), name="wishlist"),
    path("order", OrderApi.as_view(), name="orders"),
    path("order_by_status", OrderByStatus.as_view(), name="order_by_status"),
    path("update_order_status/<int:pk>", UpdateStatus.as_view(), name="update_order_status"),
    path("address", AddressApi.as_view(), name="address"),
    path("address/<int:pk>", AddressUpdateApi.as_view(), name="address_id"),
    path("order/<int:pk>", UpdateStatus.as_view(), name="update_status"),
    path("login", login_with_ph_number, name="login"),
    path("details", UserDetails.as_view(), name="details"),
    path("change_password", change_password, name="change_password"),
    path("register", RegisterView.as_view(), name="register"),
    path("verify_otp", verify_otp, name="verify_otp"),
    path("resend_otp", resend_otp, name="resend_otp"),
    path("profile_pic", UploadProfilePic.as_view(), name="profile"),
    path("forget_password", forget_password, name="forget_password"),
    path("verify_otp_forget_password", change_password_forget, name="verify_otp_forget_password"),
]
