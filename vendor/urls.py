from django.urls import path
from .views import *

urlpatterns = [
    path("products", ProductWithReviewsCount.as_view(), name="product_with_reviews_count"),
    path("earnings", EarningsVendor.as_view(), name="earnings"),
    path("products", ProductApiVendor.as_view(), name="products"),
    path("update_delete_product/<int:pk>", ProductUpdateDeleteAPi.as_view(), name="update_delete_product"),
    path("options", OptionAPi.as_view(), name="options"),
    path("update_delete_option/<int:pk>", OptionUpdateDeleteApi.as_view(), name="update_delete_option"),
    path("image", ProductImageAPi.as_view(), name="image"),
    path("delete_image", ProductImageDelete.as_view(), name="delete_image"),
]

