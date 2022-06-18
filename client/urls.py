from django.urls import path
from .views import *

urlpatterns = [
    path('topdeal', TopDeal.as_view(), name="topdeal"),
    path('season', TopViewOfHomePage.as_view(), name="top"),
    path('top_brands', TopBrandView.as_view(), name="top_brands"),
    path('product/<pk>', ProductPageView.as_view(), name="product"),
    path('recommended_products', RecommendedForYou.as_view(), name="recommended"),
    path('banners', Banners.as_view(), name="banners"),
]