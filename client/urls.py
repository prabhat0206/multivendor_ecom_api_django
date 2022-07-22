from django.urls import path
from .views import *

urlpatterns = [
    path('topdeal', TopDeal.as_view(), name="topdeal"),
    path('season', TopViewOfHomePage.as_view(), name="top"),
    path('top_brands', TopBrandView.as_view(), name="top_brands"),
    path('product/<pk>', ProductPageView.as_view(), name="product"),
    path('recommended_products', RecommendedForYou.as_view(), name="recommended"),
    path('banners', Banners.as_view(), name="banners"),
    path('search', SearchPageView.as_view(), name="search"),
    path('sub_product/<int:pk>', ProductBySubCategory.as_view(), name="sub_product"),
    path('category/<int:pk>', ProductByCategory.as_view(), name="category"),
    path('search_params', get_search_parameter, name="search_params"),
    path('category_list', CategoryByOrders.as_view(), name="category_list"),
    path('sub_category_list', SubCategoryByOrders.as_view(), name="sub_category_list"),
    path('reviews', ReviewsByProductApi.as_view(), name="reviews"),
    path('reviews_by_brand/<int:pk>', ReviewsByBrand.as_view(), name="reviews_by_brand"),
    path('product_by_brand/<int:pk>', ProductByBrand.as_view(), name="product_by_brand"),
    path('order_id', OrderID.as_view(), name="order_id"),
]