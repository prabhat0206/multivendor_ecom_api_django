from rest_framework.generics import ListCreateAPIView
from adminn.models import Review
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from adminn.serializers import ReviewSerializer


class ReviewsByProductApi(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        product_id = self.request.GET['product_id']
        return self.queryset.filter(product=product_id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
