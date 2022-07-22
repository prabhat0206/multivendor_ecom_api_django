from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from adminn.models import Review
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from adminn.serializers import ReviewSerializer
from django.conf import settings
from rest_framework.permissions import AllowAny

class ReviewsByProductApi(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        product_id = self.request.GET['product_id']
        return self.queryset.filter(product=product_id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderID(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        order = settings.CLIENT.order.create({
            "amount": float(request.GET.get("amount")) * 100,
            "currency": "INR",
            "receipt": "#1receipt",
            "notes": {
                "note1": "payment"
            }
        })
        return Response({'success': True, "order_id": order['id']})
