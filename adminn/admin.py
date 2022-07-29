from django.contrib import admin
from .models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "is_deleted"]


class BrandAdmin(admin.ModelAdmin):
    list_display = ["name", "is_deleted"]


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "is_deleted"]


class GenderAdmin(admin.ModelAdmin):
    list_display = ["name"]


# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Product)
admin.site.register(Option)
admin.site.register(ProductImage)
admin.site.register(Review)
admin.site.register(Gender, GenderAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Banner)
admin.site.register(HomePageModel)
admin.site.register(Sales)