from dataclasses import field
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import DeliveryBoy
from client.models import Order, MidOrder, OrderStatus


class DeliveryBoySerializer(ModelSerializer):
    class Meta:
        model = DeliveryBoy
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}, 'added_by': {'write_only': True}}


class OrderSerializer(ModelSerializer):
    user_name = SerializerMethodField()
    ph_number = SerializerMethodField()

    class Meta:
        model = Order
        fields = ["oid", "address", "payment_method", "user_name", "ph_number"]

    def get_user_name(self, instance):
        return instance.address.split(", ")[0]
    
    def get_ph_number(self, instance):
        return instance.address.split(", ")[-1]
    

class MidOrderSerializer(ModelSerializer):
    order = OrderSerializer()
    
    class Meta:
        model = MidOrder
        fields = ["mid", "product_price", "is_canceled", "status", "order", "delivered_assigned_day"]
