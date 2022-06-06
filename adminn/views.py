from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser


class CreateWithAuthentication(generics.ListCreateAPIView):

    permission_classes = [IsAdminUser]

    def post(self, request):
        data = request.data
        data['vendor'] = request.user.id
        serialized = self.serializer_class(data=data)
        if serialized.is_valid():
            serialized.save()
            return Response({"success": True, "data": serialized.data})
        else:
            return Response({"success": False, "error": serialized.errors})


class CategoryApi(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAdminUser]


class UpdateDeleteCategoryApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer 
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAdminUser]


class SubCategoryApi(generics.ListCreateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAdminUser]


class UpdateDeleteSubCategoryApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAdminUser]


class ProductApi(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



class UpdateDeleteProductApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAdminUser]


class GenderApi(generics.ListCreateAPIView):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAdminUser]


class UpdateDeleteGenderApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAdminUser]


class BrandApi(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAdminUser]


class UpdateDeleteBrandApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAdminUser]

