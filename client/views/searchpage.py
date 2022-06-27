from rest_framework.generics import ListAPIView
from adminn.models import Brand, Gender
from adminn.serializers import BrandSerializer, GenderSerializer
from client.models import Product
from django.db import models
from client.serializer import ProductWithOptionSerializer
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response


# get search parameter for products
@api_view(["GET"])
def get_search_parameter(request):
    query = request.GET.get('query')
    top_brands = Brand.objects.filter(product__name__icontains=query).order_by("-orders")[:5]
    genders = Gender.objects.all()
    return Response({
        "top_brands": BrandSerializer(top_brands, many=True).data,
        "genders": GenderSerializer(genders, many=True).data
    })

class SearchPageView(ListAPIView):
    queryset = Product.objects.all().filter(is_deleted=False)
    serializer_class = ProductWithOptionSerializer

    def get(self, request):
        query = request.GET.get('q', "")
        brand = request.GET.get('brand')
        price = request.GET.get('price')
        # size = request.GET.get('size')
        # color = request.GET.get('color')
        gender = request.GET.get('gender')
        sort_by = request.GET.get('sort_by')
        self.queryset = self.queryset
        if query:
            q_filter = Q(name__icontains=query) | Q(brand__name__icontains=query) | Q(category__name__icontains=query) | Q(subcategory__name__icontains=query) | Q(description__icontains=query) | Q(specification__icontains=query)
            self.queryset = self.queryset.filter(q_filter)
        if brand:
            self.queryset = self.queryset.filter(brand=brand)
        if price:
            self.queryset = self.queryset.filter(sale_price__gte=price)
        if gender:
            self.queryset = self.queryset.filter(gender__name__in=["all", gender])
        if sort_by:
            if sort_by == "desc":
                self.queryset = self.queryset.order_by("-sale_price")
            elif sort_by == "asc":
                self.queryset = self.queryset.order_by("sale_price")
        else:
            self.queryset = self.queryset.order_by("-orders")
        return self.list(request)

