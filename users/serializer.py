from dataclasses import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from client.models import Cart, MidOrder, Order, OrderStatus
from .models import Address
from adminn.serializers import ProductSerializer, OptionSerializer, ImageSerializer


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    # address_set = AddressSerializer(many=True)
    
    class Meta:
        model = User
        exclude = ['user_permissions', 'groups']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class OptionSerializerWithProduct(OptionSerializer):
    product = ProductSerializer()
    productimage_set = ImageSerializer(many=True)


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartWithProductSerializer(CartSerializer):
    option = OptionSerializerWithProduct()


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class MidOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MidOrder
        fields = '__all__'


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = '__all__'


class OrderWithLimit(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["oid", "address", "payment_method", "date_time"]


class MidOrderWithStatusSerializer(MidOrderSerializer):
    orderstatus_set = OrderStatusSerializer(many=True)
    order = OrderWithLimit()


class OrderWithMidOrder(OrderSerializer):
    midorder_set = MidOrderSerializer(many=True)

