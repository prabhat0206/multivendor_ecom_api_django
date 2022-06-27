from urllib import response
from adminn.models import *
from rest_framework import generics
# from django.db.models import Max, Min, F
from client.serializer import *
from rest_framework.response import Response
from datetime import datetime
import random
from client.models import MidOrder

class TopDeal(generics.ListAPIView):
    queryset = Product.objects.all().filter(is_deleted=False)
    serializer_class = SubCategoryWithOffer

    def get(self, request):
        instance = self.get_queryset().order_by('-discount')
        subcategories = []
        for data in instance:
            if data.subcategory not in subcategories:
                subcategories.append(data.subcategory)
        serialized = self.serializer_class(subcategories, many=True)
        paginated = self.paginate_queryset(serialized.data)
        return self.get_paginated_response(paginated)


class TopViewOfHomePage(generics.ListAPIView):
    
    queryset = Product.objects.all().filter(is_deleted=False)
    serializer_class = SubCategoryWithOffer

    def get(self, request):
        current_month = datetime.now().month
        keys = [{"key": "Footwear", "name": "Footwear"}, {"key":"Clothing & Accessories", "name": "Indian Ethic Wear"}, {"key": "Electronics", "name": "Cool down the Heat"}]
        filter_key = "Summer" if current_month > 3 and current_month < 9 else "Winter"
        response = []
        random.shuffle(keys)
        for key in keys:
            category = Category.objects.filter(name=key.get("key")).first()
            footwear_products = self.get_queryset().filter(category=category)\
                .filter(season__in=['all', filter_key.lower()])\
                    .order_by('-orders').order_by('-discount').all()
            sub_categories = []
            for product in footwear_products:
                if len(sub_categories) == 4:
                    break
                if product.subcategory not in sub_categories:
                    sub_categories.append(product.subcategory)
            serialized_subCategory = {
                "title": "Super {} sale | {}".format(filter_key, key.get("name")),
                "products": self.serializer_class(sub_categories, many=True).data
            }
            response.append(serialized_subCategory)
        return Response(response)


class ProductPageView(generics.RetrieveAPIView):
    
    queryset = Product.objects.all().filter(is_deleted=False)
    serializer_class = ProductWithReviewAndOption


class RecommendedForYou(generics.ListAPIView):
    queryset = Product.objects.all().filter(is_deleted=False)
    serializer_class = SubCategoryWithOffer

    def get(self, request):
        instance = self.get_queryset().annotate(wishlisted=models.Count('user')).order_by('-wishlisted')

        if request.user:
            instance_orders = MidOrder.objects.all().filter(order__user=request.user).order_by('-id')
            for data in instance_orders:
                if data.subcategory not in subcategories:
                    subcategories.append(data.subcategory)
            for data in instance:
                if data.subcategory not in subcategories:
                    subcategories.append(data.subcategory)
            serialized = self.serializer_class(subcategories, many=True)
            paginated = self.paginate_queryset(serialized.data)
            return self.get_paginated_response(paginated)
        
        subcategories = []
        for data in instance:
            if data.subcategory not in subcategories:
                subcategories.append(data.subcategory)
        serialized = self.serializer_class(subcategories, many=True)
        paginated = self.paginate_queryset(serialized.data)
        return self.get_paginated_response(paginated)


class TopBrandView(generics.ListAPIView):

    queryset = Brand.objects.all().order_by('-orders').filter(is_deleted=False)
    serializer_class = BrandSerializerWithOffer


class CategoryAPi(generics.ListAPIView):

    queryset = Category.objects.all().order_by('-orders').filter(is_deleted=False)
    serializer_class = CategorySerializer


class SubCategoryAPi(generics.ListAPIView):

    queryset = SubCategory.objects.all().order_by('-orders').filter(is_deleted=False)
    serializer_class = SubCategorySerializer


class ProductBySubCategory(generics.ListAPIView):

    queryset = SubCategory.objects.all().filter(is_deleted=False)
    serializer_class = ProductWithOptionSerializer

    def get_queryset(self):
        try:
            queryset = self.queryset.filter(scid=self.kwargs.get("pk")).first().product_set.filter(is_deleted=False).order_by('-orders')
            return queryset
        except:
            return []


class ProductByCategory(ProductBySubCategory):
    queryset = Category.objects.all().filter(is_deleted=False)

    def get_queryset(self):
        try:
            queryset = self.queryset.filter(cid=self.kwargs.get("pk")).first().product_set.filter(is_deleted=False).order_by('-orders')
            return queryset
        except:
            return []


class Banners(generics.ListAPIView):
    queryset = Banner.objects.all().filter(name="homepage")
    serializer_class = BannerSerializer
    pagination_class = None


