from django.db import models
from users.models import User
import string, random

class Banner(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='banners')
    name = models.CharField(max_length=255)


class Category(models.Model):
    cid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='category')
    orders = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)


class SubCategory(models.Model):
    scid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='subcategory')
    orders = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)


class Brand(models.Model):
    bid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    orders = models.IntegerField(default=0)
    image = models.ImageField(upload_to='brands')
    is_deleted = models.BooleanField(default=False)


class Gender(models.Model):
    name = models.CharField(max_length=255)


def calcuate_discount(data):
    return ((data.actual_price - data.sale_price) / data.actual_price) * 100

def generate_slug(name):
    slug = name.replace(' ', '-') + '-' 
    for _ in range(0,8):
        slug += random.choice(string.ascii_letters)
    slug += "-"
    for _ in range(8):
        slug += random.choice(string.ascii_uppercase)
    return slug


class Product(models.Model):
    pid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    specification = models.TextField()
    tags = models.TextField(blank=True, null=True)
    actual_price = models.IntegerField()
    sale_price = models.IntegerField()
    discount = models.IntegerField(blank=True, null=True)
    orders = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True, blank=True)
    season = models.CharField(max_length=100, default='all')
    user = models.ManyToManyField(User, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="of_products")

    def save(self, *args, **kwargs):
        self.tag = self.description.split(' ')
        self.discount = calcuate_discount(self)
        self.category = self.subcategory.category
        if not self.slug:
            self.slug = generate_slug(self.name)
        super(Product, self).save(*args, **kwargs)
    

class Option(models.Model):
    id = models.AutoField(primary_key=True)
    color = models.CharField(max_length=255)
    unit_size = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    in_stock = models.IntegerField(default=100)
    is_deleted = models.BooleanField(default=False)


class ProductImage(models.Model):
    img_id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='product')
    option = models.ForeignKey(Option, on_delete=models.CASCADE)


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    reviewer_name = models.CharField(max_length=255)
    reviewer_message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.DecimalField(decimal_places=1, max_digits=2, default=1.0)
    is_verified = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
