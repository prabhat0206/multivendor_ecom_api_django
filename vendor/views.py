from rest_framework import generics, response, permissions, views
from adminn.models import *
from adminn.serializers import *
from client.models import MidOrder
from client.serializer import ProductWithOptionSerializer


class ProductWithReviewsCount(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductWithOptionSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return super().get_queryset().filter(vendor=self.request.user)


class ReviewsViewByProduct(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return super().get_queryset().filter(product__vendor=self.request.user).order_by('-id')


class EarningsVendor(views.APIView):

    permission_classes = [permissions.IsAdminUser]

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

