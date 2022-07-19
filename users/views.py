from rest_framework import generics
from rest_framework.views import APIView
from adminn.models import Product
from client.serializer import ProductWithOptionSerializer
from .serializer import *
from adminn.serializers import ProductSerializer
from .models import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from adminn.models import Option
from rest_framework.decorators import api_view, permission_classes


class UserDetails(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        return Response(self.serializer_class(request.user).data)


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AddressApi(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def post(self, request):
        data = request.data
        data["user"] = request.user.id
        serialized = self.serializer_class(data=data)
        if serialized.is_valid():
            serialized.save()
            return Response({"success": True, "data": serialized.data})
        return Response({"success": False, "error": serialized.errors})


class AddressUpdateApi(generics.UpdateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]


class OrderApi(generics.ListCreateAPIView):
    queryset = MidOrder.objects.all()
    serializer_class = MidOrderWithStatusSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(order__user=self.request.user)

    def post(self, request):
        data = request.data
        if not data or "products" not in data:
            return Response(400)
        data["user"] = request.user.id
        products = data.pop("products")
        address = Address.objects.filter(address_id=data.pop("address_id")).first()
        if not address:
            return Response({"success": False, "error": "Invalid address"})
        
        # TODO: ADD RAZORPAY CHECK
        if data.get("payment_method") != "COD":
            pass
        
        data["address"] = f"{address.name}, {address.address_1}, {address.address_2}, {address.city}, {address.state}, {address.country}, {address.ph_number}"
        order = OrderSerializer(data=data)
        total_amount = 0
        if order.is_valid():
            order.save()
            for product in products:
                if "id" not in product:
                    continue
                option = Option.objects.filter(id=product["id"]).first()
                if option:
                    mid_order = {
                        "product": option.id,
                        "order": order.data["oid"],
                        "unit_size": option.unit_size,
                        "product_price": option.product.sale_price,
                        "quantity": product["quantity"],
                    }
                    mid = MidOrderSerializer(data=mid_order)
                    if mid.is_valid():
                        mid.save()
                        status = OrderStatusSerializer(data={"status": "order_placed", "midorder": mid.data["mid"]})
                        if status.is_valid():
                            status.save()
                        option.in_stock = option.in_stock - int(product["quantity"])
                        option.save()
                        product = option.product
                        product.orders += 1
                        product.save()
                        brand = product.brand
                        brand.orders += 1
                        brand.save()
                        category = product.category
                        category.orders += 1
                        category.save()
                        subcategory = product.subcategory
                        subcategory.orders += 1
                        subcategory.save()
                        total_amount += option.product.sale_price * int(mid.data["quantity"])
                    else:
                        print(mid.errors)
            created_order = Order.objects.get(oid=order.data["oid"])
            created_order.total_amount = total_amount
            created_order.save()
            return Response({"success":True, "data": OrderWithMidOrder(created_order).data})
        return Response({"success": False, "error": order.errors})


class UpdateStatus(generics.UpdateAPIView):
    queryset = MidOrder.objects.all()
    serializer_class = MidOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return super().get_object().filter(user=self.request.user).filter(mid=self.kwargs.get("pk")).first()


class CartApi(APIView):

    queryset = Cart.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CartWithProductSerializer
    
    def get(self, request):
        cart = request.user.cart_set.all()
        return JsonResponse({"cart": self.serializer_class(cart, many=True).data}, safe=False)

    def post(self, request):
        cart = request.user.cart_set.all()
        option = Option.objects.filter(id=request.data.get("id")).first()
        if option in cart:
            return JsonResponse({"success": False, "error": "Product already in cart"})
        data = request.data
        data["option"] = data.pop("id")
        data["product"] = option.product.pid
        data["user"] = request.user.id
        serialized = CartSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            return JsonResponse({"success": True, "data": serialized.data}, safe=False)
        return JsonResponse({"success": False, "error": serialized.errors}, safe=False)
    
    def put(self, request):
        try:
            cart_product = request.user.cart_set.all().get(id=request.data.get("id"))
        except:
            return HttpResponse(404)
        if cart_product:
            cart_product.quantity = request.data.get("quantity", 1)
            cart_product.save()
            return JsonResponse({"success": True}, safe=False)
        else: return HttpResponse(404)
    
    def delete(self, request):
        cart_product = request.user.cart_set.all().get(id=request.GET.get("id"))
        if cart_product:
            cart_product.delete()
            return JsonResponse({"success": True}, safe=False)
        return HttpResponse(404)


class WishList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = request.user.product_set.all()
        return JsonResponse(ProductWithOptionSerializer(data, many=True).data, safe=False)

    def post(self, request):
        wishlist_products = request.user.product_set
        try:
            product = Product.objects.get(pid=request.GET.get("pid"))
        except:
            return HttpResponse(404)
        if product:
            if product not in wishlist_products.all():
                wishlist_products.add(product)
                return JsonResponse({"success": True}, safe=False)
            return HttpResponse(409)
        return HttpResponse(404)

    def delete(self, request):
        wishlist_products = request.user.product_set
        try:
            is_exist = wishlist_products.get(pid=request.GET.get('pid'))
        except:
            return HttpResponse(404)
        if is_exist:
            wishlist_products.remove(is_exist)
            return JsonResponse({"success": True}, safe=False)
        return HttpResponse(404)


@api_view(['POST'])
@permission_classes((AllowAny,))
def login_with_ph_number(request):
    data = request.data
    user = User.objects.filter(ph_number=data.get('ph_number')).first()
    if (user):
        if user.check_password(data["password"]):
            try:
                return Response({"success": True, "token": user.auth_token.key, "user": UserSerializer(user).data})
            except Exception as e:
                print(e)
    return Response({"success": False, "error": "Server unable to authenticate you"})


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def change_password(request):
    data = request.data
    user = request.user
    if (user):
        if user.check_password(data["old_password"]):
            user.set_password(data["new_password"])
            user.save()
            return Response({"success": True})
    return Response({"success": False, "error": "Server unable to authenticate you"})
