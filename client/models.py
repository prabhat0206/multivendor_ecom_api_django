from itertools import product
from django.db import models

# Create your models here.
from adminn.models import Product, Option
from delivery.models import DeliveryBoy
from users.models import User


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Order(models.Model):
    oid = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.TextField()
    payment_method = models.CharField(max_length=100)
    total_discount = models.FloatField(default=0)
    rz_payment_id = models.CharField(max_length=100, null=True, blank=True)
    rz_order_id = models.CharField(max_length=100, null=True, blank=True)
    total_amount = models.FloatField(default=0)
    date_time = models.DateTimeField(auto_now_add=True)
    discount = models.IntegerField(default=0)
    redeemed_points = models.IntegerField(default=0)
    coupon_id = models.CharField(max_length=255, blank=True, null=True)
    # wallet_balance_use = models.PositiveIntegerField(default=0)


class MidOrder(models.Model):
    mid = models.AutoField(primary_key=True)
    product = models.ForeignKey(Option, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_price = models.FloatField()
    quantity = models.PositiveIntegerField(default=1)
    product_discount = models.FloatField(default=0)
    is_canceled = models.BooleanField(default=False)
    status = models.CharField(max_length=255, default="order_placed")
    delivered_by = models.ForeignKey(DeliveryBoy, on_delete=models.SET_NULL, null=True, blank=True)
    delivered_assigned_day = models.DateTimeField(null=True, blank=True)


class OrderStatus(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=255)
    date_time = models.DateTimeField(auto_now_add=True)
    midorder = models.ForeignKey(MidOrder, on_delete=models.CASCADE)


class Coupon(models.Model):
    id = models.AutoField(primary_key=True)
    coupon_code = models.CharField(max_length=255)
    discount = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    date_time = models.DateTimeField(auto_now_add=True)
    valid_till = models.DateTimeField()
