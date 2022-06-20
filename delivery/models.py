from dataclasses import fields
from pyexpat import model
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from users.models import User
# Create your models here.

class DeliveryBoy(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300)
    email = models.EmailField(max_length=300, default="email@example.com")
    ph_number = PhoneNumberField()
    password = models.CharField(max_length=200)
    is_offline = models.BooleanField(default=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    address = models.TextField()
    profile_pic = models.ImageField(upload_to="delivery_boy", null=True, blank=True)