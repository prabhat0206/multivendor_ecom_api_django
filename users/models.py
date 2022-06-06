from pydoc import describe
from django.db import models
# from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import random
import string

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


def generate_referel_code():
    number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    code = ""
    for _ in range(0, 4):
        code += random.choice(string.ascii_uppercase)
        code += random.choice(number)
    return code.upper()

class UserManager(BaseUserManager):
    def create_user(self, name, email, ph_number, username, password=None):
        if username is None:
            raise TypeError('User name is required')
        if name is None:
            raise TypeError('Users should have a Name')
        if ph_number is None:
            raise TypeError('Users should have a phone number')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(name=name, email=self.normalize_email(
            email), ph_number=ph_number, username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, name, email, ph_number, username, password):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(name, email, ph_number, username)
        user.set_password(password)
        user.superuser = True
        user.staff = True

        user.save()
        return user

    def create_staff(self, name, email, ph_number, username, password):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(name, email, ph_number, username)
        user.set_password(password)
        user.superuser = False
        user.staff = True

        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    profile_pic = models.ImageField(upload_to="profile", null=True, blank=True)
    ph_number = PhoneNumberField(unique=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    superuser = models.BooleanField(default=False)
    delivery_boy = models.BooleanField(default=False)
    referal_code = models.CharField(max_length=10, null=True, blank=True)
    earned_points = models.IntegerField(default=0)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['ph_number', 'name', 'email']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = Token.for_user(self)
        return {
            'token': str(refresh)
        }

    @property
    def is_superuser(self):
        return self.superuser

    @property
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_delivery_boy(self):
        return self.delivery_boy

    def save(self, *args, **kwargs):
        if not (self.referal_code):
            self.referal_code = generate_referel_code()
        super(User, self).save(*args, **kwargs)


class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address_1 = models.TextField()
    address_2 = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    ph_number = PhoneNumberField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class VendorShop(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    vendor = models.OneToOneField(User, on_delete=models.CASCADE)

