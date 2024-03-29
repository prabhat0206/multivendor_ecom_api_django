from django.db import models
from users.models import User
import string, random
from typing import Any


class CustomManager(models.Manager):
    
    def all(self):
        return super().all().exclude(is_deleted=True)
    
    def filter(self, *args: Any, **kwargs: Any):
        return super().filter(*args, **kwargs).exclude(is_deleted=True)
    
    def get(self, *args: Any, **kwargs: Any):
        return super().exclude(is_deleted=True).get(*args, **kwargs)
    
    
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
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomManager()

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    scid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='subcategory')
    orders = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomManager()

    def __str__(self):
        return self.name

class Brand(models.Model):
    bid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    orders = models.IntegerField(default=0)
    description = models.TextField(default='')
    image = models.ImageField(upload_to='brands')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    objects = CustomManager()


class Gender(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

def calcuate_discount(data):
    return ((data.actual_price - data.sale_price) / data.actual_price) * 100

def generate_slug(name):
    slug = name.replace(' ', '-').replace("/", "") + '-'
    slug = slug if len(slug) < 20 else slug[:20]
    for _ in range(0,8):
        slug += random.choice(string.ascii_letters)
    slug += "-"
    for _ in range(8):
        slug += random.choice(string.ascii_uppercase)
    return slug.lower()


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
    expected_pincodes = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True, blank=True)
    season = models.CharField(max_length=100, default='all')
    user = models.ManyToManyField(User, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="of_products", null=True, blank=True)

    objects = CustomManager()

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
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    objects = CustomManager()


class ProductImage(models.Model):
    img_id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='product')
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.product = self.option.product
        super(ProductImage, self).save(*args, **kwargs)


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews", null=True, blank=True)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.DecimalField(decimal_places=1, max_digits=2, default=1.0)
    is_verified = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)


CHOICES = (
    ("top", "Top Region"),
    ("bottom", "Bottom Region"),
)

class HomePageModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255, choices=CHOICES)
    categories = models.ManyToManyField(Category)


class Sales(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

