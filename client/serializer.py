from rest_framework.serializers import *
from adminn.models import *
from adminn.serializers import *


class OptionSerializerWithImage(OptionSerializer):
    productimage_set = ImageSerializer(many=True)
    class Meta:
        model = Option
        fields = '__all__'


class ProductWithOptionSerializer(ProductSerializer):
    option_set = OptionSerializerWithImage(many=True)
    review_count = SerializerMethodField()

    def get_review_count(self, instance):
        return len(instance.review_set.all())


class ProductWithReviewAndOption(ProductWithOptionSerializer):
    review_set = ReviewSerializer(many=True)


class ProductByGender(GenderSerializer):
    product_set = ProductSerializer(many=True)


class SubCategoryWithProducts(SubCategorySerializer):

    product_set = SerializerMethodField()

    def get_product_set(self, instance):
        return ProductWithOptionSerializer(instance.product_set.order_by('-orders'), many=True).data


class CategoryWithSubCategory(CategorySerializer):

    subcategory_set = SerializerMethodField()

    def get_subcategory_set(self, instance):
        return SubCategory(instance.subcategory_set.order_by('-orders'), many=True).data


class BrandWithProducts(BrandSerializer): 
    product_set = ProductWithOptionSerializer(many=True)



class CategoryWithOffer(CategorySerializer):
    max_price = SerializerMethodField()
    min_price = SerializerMethodField()
    product = SerializerMethodField()
    
    def get_max_price(self, instance):
        max_price = instance.product_set.aggregate(models.Max('sale_price'))
        return max_price

    def get_min_price(self, instance):
        min_price = instance.product_set.aggregate(models.Min('sale_price'))
        return min_price

    def get_product(self, instance):
        product = ProductWithOptionSerializer(instance.product_set.order_by('-orders').first()).data
        return product


class SubCategoryWithOffer(SubCategorySerializer):
    max_discount = SerializerMethodField()
    min_discount = SerializerMethodField()
    product = SerializerMethodField()
    image = SerializerMethodField()
    
    def get_max_discount(self, instance):
        max_price = instance.product_set.aggregate(models.Max('discount'))
        return max_price

    def get_min_discount(self, instance):
        min_price = instance.product_set.aggregate(models.Avg('discount'))
        return min_price

    def get_product(self, instance):
        product = ProductWithOptionSerializer(instance.product_set.order_by('-orders').first()).data
        return product
    
    def get_image(self, instance):
        try:
            image = instance.product_set.order_by('-orders')\
                .first().option_set.first()\
                    .productimage_set.first().image.url
        except:
            image = instance.image.url
        return image


class BrandSerializerWithOffer(BrandSerializer):
    max_price = SerializerMethodField()
    min_price = SerializerMethodField()
    product = SerializerMethodField()
    products_count = SerializerMethodField()
    
    def get_max_price(self, instance):
        max_price = instance.product_set.aggregate(models.Max('sale_price'))
        return max_price

    def get_min_price(self, instance):
        min_price = instance.product_set.aggregate(models.Min('sale_price'))
        return min_price

    def get_product(self, instance):
        product = ProductWithOptionSerializer(instance.product_set.order_by('-orders').first()).data
        return product
    
    def get_products_count(self, instance):
        return instance.product_set.count()

