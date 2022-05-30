from rest_framework.generics import ListAPIView
from client.models import Product
from django.db import models
from client.serializer import ProductWithOptionSerializer

class SearchProduct(ListAPIView):
    queryset = Product.objects.all()
    serializer = ProductWithOptionSerializer

    def get(self, request):
        pass
