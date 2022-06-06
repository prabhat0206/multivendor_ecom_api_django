from django.urls import path
from .views import *

urlpatterns = [
    path("products", ProductWithReviewsCount.as_view(), name="product_with_reviews_count"),
    path("earnings", EarningsVendor.as_view(), name="earnings"),
]

