from os import stat
from rest_framework.generics import ListAPIView
from functools import wraps
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from client.models import MidOrder, OrderStatus
from .models import DeliveryBoy
from .serializers import DeliveryBoySerializer, MidOrderSerializer
from rest_framework.decorators import api_view, permission_classes
from django.utils.decorators import method_decorator
import jwt
from django.conf import settings

def encode_token(user):
    return jwt.encode(DeliveryBoySerializer(user).data, settings.SECRET_KEY, algorithm="HS256")

def check_delivery_auth(next):
    @wraps(next)
    def check_auth(request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if token:
            token = token.replace('Delivery ', '')
            try:
                decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                if decoded_token.get("ph_number"):
                    delivery_boy = DeliveryBoy.objects.filter(ph_number=decoded_token.get("ph_number")).first()
                    if delivery_boy:
                        request.user = delivery_boy
                        return next(request, *args, **kwargs)
                    else:
                        return Response(401)
                else:
                    return Response(401)
            except Exception as e:
                print(e)
                return Response(401)
        else:
            return Response(401)
    return check_auth


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    user = DeliveryBoy.objects.filter(ph_number=request.data.get('ph_number')).first()
    if user:
        if user.password == request.data.get('password'):
            return Response({"success" : True, "token": encode_token(user)})
        else:
            return Response(401)
    return Response(404)


@api_view(["GET"])
@permission_classes([AllowAny])
@check_delivery_auth
def index(request):
    return Response({"success": True})


@api_view(["PATCH"])
@permission_classes([AllowAny])
@check_delivery_auth
def checkout_checkin(request):
    user = request.user
    try:
        user.is_offline = request.GET.get('status')
        user.save()
        return Response(200)
    except:
        return Response(400)


class OrderByDeliveryBoy(ListAPIView):
    queryset = MidOrder.objects.all()
    serializer_class = MidOrderSerializer

    @method_decorator(check_delivery_auth)
    def get(self, request):
        instance = self.get_queryset().filter(delivered_by=request.user).order_by("-mid")
        serialized = self.serializer_class(instance, many=True)
        pagniated = self.paginate_queryset(serialized.data)
        return self.get_paginated_response(pagniated)


class OrderByStatus(ListAPIView):
    queryset = MidOrder.objects.all()
    serializer_class = MidOrderSerializer

    def get_queryset(self):
        return super().get_queryset().filter(status=self.kwargs.get("status"))

    @method_decorator(check_delivery_auth)
    def get(self, request, status):
        instance = self.get_queryset().filter(delivered_by=request.user).order_by("-mid")
        serialized = self.serializer_class(instance, many=True)
        pagniated = self.paginate_queryset(serialized.data)
        return self.get_paginated_response(pagniated)


@api_view(["PUT"])
@permission_classes([AllowAny])
@check_delivery_auth
def update_order_status(request):
    try:
        data = request.GET
        order = MidOrder.objects.filter(mid=data["mid"]).first()
        if not order:
            return Response(404)
        if order.delivered_by != request.user:
            return Response(401)
        order.status = data["status"]
        order.save()
        new_status = OrderStatus(status=order.status, midorder=order)
        new_status.save()
        return Response(MidOrderSerializer(order).data)
    except Exception as e:
        print(e)
        return Response(500)


@api_view(["GET"])
@permission_classes([AllowAny])
@check_delivery_auth
def delivery_details(request):
    data = DeliveryBoySerializer(request.user).data
    data["total_delivered"] = len(request.user.midorder_set.filter(status__in=["delivered", "compleated"]))
    return Response(data)

