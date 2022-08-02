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
from django.core.mail import send_mail
from rest_framework.parsers import FormParser, MultiPartParser
import vonage, os
from django.conf import settings
print(f"EMAIL_HOST = {settings.EMAIL_HOST}")

client = vonage.Client(key=os.environ.get("SMS_KEY"), secret=os.environ.get("SMS_SECRET"))
sms = vonage.Sms(client)


def generate__otp():
    otp = random.randint(100000, 999999)
    return otp


def send_otp(ph_number, otp):
    response = sms.send_message({
        'from': 'VIMANI',
        'to': ph_number,
        'text': f"Your OTP is {otp}",
    })
    return response


def send_email(email, subject, otp):
    message = f"This is verification code for your vimani account.\n\n{otp}"
    send_mail(subject, message, 'Vimani Pvt. <noreply@codencrafts.live>', [email], fail_silently=False)


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

    def post(self, request):
        data = request.data
        data["is_email_verified"] = False
        data["is_mobile_verified"] = False
        data["active"] = False
        data["last_otp_email"] = generate__otp()
        data["last_otp_ph_number"] = generate__otp()
        serializer = self.serializer_class(data=data)
        res = send_otp(data["ph_number"], data["last_otp_ph_number"])
        print(res)
        if res["messages"][0]["status"] != "0":
            return Response({"error": "Something went wrong. Please try again later."})
        if serializer.is_valid():
            serializer.save()
            send_email(data["email"], "Vimani OTP", data["last_otp_email"])
            return Response(serializer.data)
        return Response(serializer.errors)


@api_view(['POST'])
@permission_classes((AllowAny,))
def verify_otp(request):
    data = request.data
    user = User.objects.get(ph_number=data["ph_number"])
    email_verified = user.is_email_verified
    mobile_verified = user.is_mobile_verified
    if user.last_otp_email == int(data["email_otp"]):
        user.is_email_verified = True
        user.save()
        email_verified = True
    if user.last_otp_ph_number == int(data["mobile_otp"]):
        user.is_mobile_verified = True
        user.save()
        mobile_verified = True
    if email_verified and mobile_verified:
        user.active = True
        user.save()
        return Response({"success": "Your account has been verified.", "user": UserSerializer(user).data, "token": user.auth_token.key})
    return JsonResponse({"status": "failure", "email": email_verified, "mobile": mobile_verified})


@api_view(['POST'])
@permission_classes((AllowAny,))
def resend_otp(request):
    data = request.data
    user = User.objects.get(ph_number=data["ph_number"])
    res = send_otp(str(user.ph_number).replace("+",""), user.last_otp_ph_number)
    if res["messages"][0]["status"] != "0":
        return Response({"error": "Something went wrong. Please try again later."})
    send_email(user.email, "Vimani OTP", user.last_otp_email)
    return JsonResponse({"status": "success"})


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
        
        # signature
        # rz_payment_id
        # rz_order_id
        if data['payment_method'].lower() != 'cod':
            rz_data = {
                'razorpay_order_id': data.get('rz_order_id'),
                'razorpay_payment_id': data.get('rz_payment_id'),
                'razorpay_signature': data.get('signature')
            }
            if not (settings.CLIENT.utility.verify_payment_signature(rz_data)):
                return Response({"success": False, "error": "payment id not valid"})
        
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
        return self.get_queryset().filter(order__user=self.request.user).filter(mid=self.kwargs.get("pk")).first()

    def update(self, request, *args, **kwargs):
        data = request.data
        if not data or "status" not in data:
            return Response(400)
        mid = self.get_object()
        if mid:
            if "cancel" in data["status"].lower():
                mid.is_canceled = True
            mid.status = data["status"]
            mid.save()
            status = OrderStatusSerializer(data={"status": data["status"], "midorder": mid.mid})
            if status.is_valid():
                status.save()
                return Response({"success": True, "data": status.data})
            return Response({"success": False, "error": status.errors})
        return Response({"success": False, "error": "Mid order not found"})


class OrderByStatus(generics.ListAPIView):
    queryset = MidOrder.objects.all()
    serializer_class = MidOrderWithStatusSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(order__user=self.request.user).filter(status=self.request.GET.get("status"))


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
                if user.is_email_verified and user.is_mobile_verified:
                    return Response({"success": True, "token": user.auth_token.key, "user": UserSerializer(user).data})
                else:
                    user.last_otp_email = generate__otp()
                    user.last_otp_ph_number = generate__otp()
                    user.save()
                    send_otp(str(user.ph_number), user.last_otp_ph_number)
                    send_email(user.email, "Vimani OTP", user.last_otp_email)
                    return Response({"success": False, "error": "Please verify your email and phone number"})
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


class UploadProfilePic(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user:
            user.profile_pic = request.FILES.get("profile_pic")
            user.save()
            return Response({"success": True})
        return Response({"success": False, "error": "Server unable to authenticate you"})


@api_view(['POST'])
@permission_classes((AllowAny,))
def forget_password(request):
    data = request.data
    user = User.objects.filter(email=data.get('email')).first()
    if (user):
        user.last_otp_email = generate__otp()
        user.save()
        send_email(user.email, "Vimani OTP", user.last_otp_email)
        return Response({"success": True})
    return Response({"success": False, "error": "Server unable to authenticate you"})


@api_view(['POST'])
@permission_classes((AllowAny,))
def change_password_forget(request):
    data = request.data
    user = User.objects.filter(email=data.get('email')).first()
    if (user):
        if user.last_otp_email == int(data.get('otp')):
            user.set_password(data["new_password"])
            user.save()
            return Response({"success": True})
    return Response({"success": False, "error": "Server unable to authenticate you"})

