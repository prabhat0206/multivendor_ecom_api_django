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
    path('brand/<int:pk>', UpdateDeleteBrandApi.as_view(), name='brand_edit')
]
