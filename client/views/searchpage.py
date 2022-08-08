from rest_framework.generics import ListAPIView
from adminn.models import Brand, Gender
from adminn.serializers import BrandSerializer, GenderSerializer
from client.models import Product
from django.db import models
from client.serializer import ProductWithOptionSerializer
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


# get search parameter for products
@api_view(["GET"])
@permission_classes([AllowAny])
def get_search_parameter(request):
    query = request.GET.get('q')
    if not query:
        return Response(400)
    sizes = Product.objects.filter(Q(brand__name__icontains=query)|Q(subcategory__name__icontains=query)|Q(category__name__icontains=query) | Q(name__icontains=query)).values_list('option__unit_size', flat=True).distinct()
    colors = Product.objects.filter(Q(brand__name__icontains=query)|Q(subcategory__name__icontains=query)|Q(category__name__icontains=query) | Q(name__icontains=query)).values_list('option__color', flat=True).distinct()
    genders = Product.objects.filter(Q(brand__name__icontains=query)|Q(subcategory__name__icontains=query)|Q(category__name__icontains=query) | Q(name__icontains=query)).values_list('gender__name', flat=True).distinct()
    brands = Product.objects.filter(Q(brand__name__icontains=query)|Q(subcategory__name__icontains=query)|Q(category__name__icontains=query) | Q(name__icontains=query)).values_list('brand__name', flat=True).distinct()
    price_range = [5000, 10000, 20000, 50000]
    return Response({
        "res": [
            {
                "name": "Top Brands",
                "value": brands,
            }, 
            {
                "name": "Genders", 
                "value": genders
            }, 
            {
                "name": "Sizes", 
                "value": sizes
            }, 
            {
                "name": "Colors", 
                "value": colors
            }, 
            {
                "name": "Price Range", 
                "value": price_range
            }
        ]
    })


class SearchPageView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductWithOptionSerializer

    def get(self, request):
        query = request.GET.get('q', "")
        brand = request.GET.get('brand')
        price = request.GET.get('price')
        size = request.GET.get('size')
        color = request.GET.get('color')
        gender = request.GET.get('gender')
        sort_by = request.GET.get('sort_by')
        sub = request.GET.get('sub')
        self.queryset = self.queryset
        if query:
            q_filter = Q(subcategory__name__icontains=query)
            if not sub:
                q_filter = q_filter | Q(brand__name__icontains=query) | Q(name__icontains=query) | Q(category__name__icontains=query) | Q(description__icontains=query) | Q(specification__icontains=query)
            self.queryset = self.queryset.filter(q_filter)
        if brand:
            self.queryset = self.queryset.filter(brand__name=brand)
        if price:
            self.queryset = self.queryset.filter(sale_price__gte=price)
        if gender:
            self.queryset = self.queryset.filter(gender__name__in=["all", gender])
        if size:
            self.queryset = self.queryset.filter(option__unit_size=size)
        if color:
            self.queryset = self.queryset.filter(option__color=color)
        if sort_by:
            if sort_by == "desc":
                self.queryset = self.queryset.order_by("-sale_price")
            elif sort_by == "asc":
                self.queryset = self.queryset.order_by("sale_price")
        else:
            self.queryset = self.queryset.order_by("-orders")
        return self.list(request)

