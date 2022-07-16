from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('login', obtain_auth_token, name='login'),
    path('category', CategoryApi.as_view(), name='category'),
    path('sub_category', SubCategoryApi.as_view(), name='sub_category'),
    path('product', ProductApi.as_view(), name='product'),
    path('category/<int:pk>', UpdateDeleteCategoryApi.as_view(), name='category_edit'),
    path('sub_category/<int:pk>', UpdateDeleteSubCategoryApi.as_view(), name='sub_category_edit'),
    path('product/<int:pk>', UpdateDeleteProductApi.as_view(), name='product_edit'),
    path('gender', GenderApi.as_view(), name='gender'),
    path('gender/<int:pk>', UpdateDeleteGenderApi.as_view(), name='gender_edit'),
    path('brand', BrandApi.as_view(), name='brand'),
    path('brand/<int:pk>', UpdateDeleteBrandApi.as_view(), name='brand_edit'),
    path('all_orders', GetAllOrders.as_view(), name='all_orders'),
    path('order_by_status/<str:status>', OrderByStatus.as_view(), name='order_by_status'),
    path('order/<int:pk>', OrderView.as_view(), name='order'),
    path('product_vendor/<int:pk>', ProductByVendor.as_view(), name='vendor_by_product' ),
    path('vendor', AddVendor.as_view(), name="add_vendor"),
    path('vendor/<int:pk>', EditDeleteVendor.as_view(), name="edit_vendor"),
    path('all_users', AllUsers.as_view(), name="all_users"),
    path('banner', BannerApi.as_view(), name="banner"),
    path('banner/<int:pk>', BannerUpdateDelete.as_view(), name="banner_edit"),
    path('option', OptionApi.as_view(), name="option"),
    path('option/<int:pk>', OptionUpdateDeleteApi.as_view(), name="option_edit"),
    path('image', ImageApi.as_view(), name="image"),
    path('image/<int:pk>', ImageUpdateDeleteApi.as_view(), name="image_edit"),
    path('all_products', AllProductApi.as_view(), name="all_products")
]
