from unicodedata import name
from django.urls import path
from .views import *

urlpatterns = [
    path('', delivery_details, name="index"),
    path('login', login, name="login"),
    path('assigned', OrderByDeliveryBoy.as_view(), name="assigned"),
    path('check_in_out', checkout_checkin, name="check_in_out"),
    path("status/<status>", OrderByStatus.as_view(), name="status"),
    path("update_status", update_order_status,name="update_status"),
]
