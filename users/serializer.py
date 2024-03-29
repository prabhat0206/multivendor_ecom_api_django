from dataclasses import fields
from rest_framework import serializers
from .models import User
from client.models import Cart, MidOrder, Order, OrderStatus
from .models import Address
from adminn.serializers import ProductSerializer, OptionSerializer, ImageSerializer


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()
    class Meta:
        model = User
        exclude = ['user_permissions', 'groups']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'superuser': {
                'write_only': True
            }, 
            'vendor': {
                'write_only': True
            }, 
            'staff': {
                'write_only': True
            }, 
            'last_otp_ph_number': {
                'write_only': True
            },
            'last_otp_email': {
                'write_only': True
            },
            'product_count': {
                'read_only': True
            },
            'request_id': {
                'write_only': True
            }
        }
    
    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def get_product_count(self, obj):
        return obj.of_products.count()


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


class UserWithLimit(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "ph_number"]


class OrderWithLimit(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ["oid", "address", "payment_method", "date_time", "user_name"]
    
    def get_user_name(self, obj):
        return obj.address.split(",")[0]


class MidOrderWithStatusSerializer(MidOrderSerializer):
    orderstatus_set = OrderStatusSerializer(many=True)
    order = OrderWithLimit()
    product = OptionSerializerWithProduct()


class OrderWithMidOrder(OrderSerializer):
    midorder_set = MidOrderSerializer(many=True)


class OrderWithUser(OrderSerializer):
    user = UserWithLimit()

class MidOrderWithOrder(MidOrderSerializer):
    order = OrderWithUser()


class MidOrderWithProductAndStatus(MidOrderSerializer):
    details = serializers.SerializerMethodField()
    orderstatus_set = OrderStatusSerializer(many=True)

    def get_details(self, obj):
        return OptionSerializerWithProduct(obj.product).data


class OrderWithMidOrderAndStatus(OrderWithUser):
    midorder_set = MidOrderWithProductAndStatus(many=True)

