from gettext import install
from operator import ge
from rest_framework.response import Response
from rest_framework import generics, response, permissions, views, parsers
from adminn.models import *
from adminn.serializers import *
from client.models import MidOrder, Order
from client.serializer import ProductWithOptionSerializer
from users.serializer import MidOrderWithOrder
from rest_framework.permissions import BasePermission


class IsVendor(BasePermission):
    def has_permission(self, request, view):
        return request.user.vendor

class CustomListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsVendor]
    
    def get_queryset(self):
        return super().get_queryset().filter(vendor=self.request.user)

    def get_object(self):
        instance = self.get_queryset().filter(pid=self.kwargs.get("pk")).first()
        if instance.vendor == self.request.vendor:
            return instance
        return Response(401)

    def perform_create(self, serializer):
        return serializer.save(vendor=self.request.user)

class SubCategoryApi(generics.ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    pagination_class = None


class BrandApi(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BannerSerializer
    pagination_class = None


class ProductApiVendor(CustomListCreateAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductUpdateDeleteAPi(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsVendor]

    def get_object(self):
        instance = self.get_queryset().filter(pid=self.kwargs.get("pk")).first()
        if instance.vendor == self.request.vendor:
            return instance
        return Response(401)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(204)


class OptionAPi(generics.ListCreateAPIView):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    permission_classes = [IsVendor]

    def post(self, request):
        data = request.data.dict()
        product = Product.objects.filter(pid=data["product"]).first()
        if product:
            if product.vendor == self.request.user:
                serialized = self.serializer_class(data=data)
                if serialized.is_valid():
                    serialized.save()
                    return Response({"success": True, "data": serialized.data})
                return Response({"sucess": False, "error": serialized.errors})
            return Response(401)
        return Response(404)


class OptionUpdateDeleteApi(generics.RetrieveUpdateDestroyAPIView):

    queryset = Option.objects.all()
    serializr_class = OptionSerializer
    permission_classes = [IsVendor]

    def get_object(self):
        instance = self.get_queryset().filter(id=self.kwargs.get("pk")).first()
        if instance.product.vendor == self.request.vendor:
            return instance
        return Response(401)

    def delete(self):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(204)


class ProductImageAPi(generics.ListCreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ImageSerializer
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]
    permission_classes = [IsVendor]

    def post(self, request):
        data = request._request.POST.dict()
        image = request._request.FILES.get("image")
        if not image:
            return Response(400)
        data["image"] = image
        option = Option.objects.filter(id=data["option"]).first()
        if option:
            if option.product.vendor == self.request.user:
                serialized = self.serializer_class(data=data)
                if serialized.is_valid():
                    serialized.save()
                    return Response({"success": True, "data": serialized.data})
                return Response({"sucess": False, "error": serialized.errors})
            return Response(401)
        return Response(404)


class ProductImageDelete(generics.DestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsVendor]

    def get_object(self):
        instance = self.get_queryset().filter(img_id=self.kwargs.get("pk")).first()
        if instance.option.product.vendor == self.request.vendor:
            return instance
        return Response(401) 


class ProductWithReviewsCount(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductWithOptionSerializer
    permission_classes = [IsVendor]

    def get_queryset(self):
        return super().get_queryset().filter(vendor=self.request.user)


class ReviewsViewByProduct(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsVendor]

    def get_queryset(self):
        return super().get_queryset().filter(product__vendor=self.request.user).order_by('-id')


class EarningsVendor(views.APIView):

    permission_classes = [IsVendor]

    def get(self, request):
        earnings = request.user.product_set\
                .filter(midorder_set__status="delivered")\
                    .annotate(total_amount=models.Sum("midorder_set__product_price"))
        print(earnings)
        res = {
            "status": "success",
            "earnings": earnings.total_amount if earnings else 0 
        }
        return response.Response(res)


class OrderByVendor(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = MidOrderWithOrder
    permission_classes = [IsVendor]

    def get_queryset(self):
        return super().get_queryset().filter(product__vendor=self.request.vendor).order_by("-mid")


class OrderByStatus(generics.ListAPIView):
    queryset = MidOrder.objects.all()
    serializer_class = MidOrderWithOrder
    permission_classes = [IsVendor]

    def get_queryset(self):
        return super().get_queryset().filter(product__vendor=self.request.user).filter(status=self.kwargs.get('status')).order_by('-mid')



