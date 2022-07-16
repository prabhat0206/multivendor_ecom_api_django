from rest_framework import generics
from client.serializer import ProductWithOptionSerializer, ProductWithReviewAndOption
from .models import *
from .serializers import *
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from client.models import Order, MidOrder
from users.serializer import MidOrderWithOrder, OrderWithMidOrderAndStatus, UserSerializer


class CreateWithAuthentication(generics.ListCreateAPIView):

    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user)


class EditDelete(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAdminUser]
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(204)


class CategoryApi(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAdminUser]


class UpdateDeleteCategoryApi(EditDelete):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubCategoryApi(generics.ListCreateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAdminUser]


class UpdateDeleteSubCategoryApi(EditDelete):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    


class ProductApi(CreateWithAuthentication):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class UpdateDeleteProductApi(EditDelete):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


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


class GetAllOrders(generics.ListAPIView):
    queryset = MidOrder.objects.all().order_by("-mid")
    serializer_class = MidOrderWithOrder
    permission_classes = [IsAdminUser]


class OrderByStatus(generics.ListAPIView):
    queryset = MidOrder.objects.all()
    serializer_class = MidOrderWithOrder
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return super().get_queryset().filter(status=self.kwargs.get('status')).order_by('-mid')


class OrderView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderWithMidOrderAndStatus
    permission_classes = [IsAdminUser]


class ProductByVendor(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductWithOptionSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return super().get_queryset().filter(vendor=self.kwargs.get('pk')).order_by('-pid')


class AddVendor(generics.ListCreateAPIView):
    queryset = User.objects.all().filter(vendor=True)
    serializer_class = UserSerializer
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(vendor=True)


class EditDeleteVendor(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAdminUser]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.vendor = False
        instance.of_products.update(is_deleted=True)
        return Response(204)


class AllUsers(generics.ListAPIView):
    queryset = User.objects.all().filter(vendor=False)
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class BannerApi(generics.ListCreateAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [FormParser, MultiPartParser]


class BannerUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [IsAdminUser]


class OptionApi(generics.ListCreateAPIView):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    permission_classes = [IsAdminUser]
    pagination_class = None


class ImageApi(generics.ListCreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ImageSerializer
    parser_classes = [FormParser, MultiPartParser]
    pagination_class = None
    permission_classes = [IsAdminUser]


class OptionUpdateDeleteApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    permission_classes = [IsAdminUser]


class ImageUpdateDeleteApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAdminUser]


class AllProductApi(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductWithReviewAndOption
    permission_classes = [IsAdminUser]
