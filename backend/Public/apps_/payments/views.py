
from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView
from rest_framework import permissions as p
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializer import PaymentCreateSerializer, PaymentSerializer, TopshirishPunktSerializer, TakerSerializer, PromotionSerializer
from .services import PaymentService
from apps_.orders.models import Order
from apps_.orders.serializers import OrderSerializer

from .models import Payment
from .services import send_verification_link
from .utils import verify_verification_token
from apps_.promotions.services import PromotionService
from apps_.promotions.models import UserUsedPromotion



class CreateTakerView(CreateAPIView):
    permission_classes = [p.IsAuthenticated]
    serializer_class = TakerSerializer
    
    def post(self, request ,order_id, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        
        order = Order.objects.get(pk=order_id)
        order.taker = serializer.instance
        order.save()
        
        return Response({'detail':'taker created'}, status=200)
    
    
class CreateTopshirishPunktView(CreateAPIView):
    permission_classes = [p.IsAuthenticated]
    serializer_class = TopshirishPunktSerializer
    
    def post(self, request,order_id, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        order = Order.objects.get(pk=order_id)
        
        serializer.save(user=user, order=order)
        return Response({'detail':'topshirish punkt created'}, status=200)
    

class GetPromotionCodeView(APIView):
    permission_classes = [p.IsAuthenticated]

    def get(self, request,order_id, code, *args, **kwargs):
        
        if not code:
            return Response({'detail':'code kelmadi'}, status=400)
        
        service = PromotionService()
        promotion = service.get_promotion_by_code(code)
        if not promotion:
            return Response({'detail':'promo code not found'}, status=404)
        
        check_promotion = service.check_user_promotion(request.user, promotion_id=promotion['id'], promotion_type=promotion['type'])
        
        if check_promotion == True:
            return Response({'detail':'promo kodni siz oldin ishlatgansiz'}, status=400)
        
       
        
        if not order_id:
            return Response({'detail':'error'}, status=status.HTTP_400_BAD_REQUEST)
        order = Order.objects.get(pk=order_id)
        price = order.discounted_price
        
        if promotion['interest']:
            promotioned_price = price - ((price * int(promotion['interest'])) / 100)
            order.discounted_price = promotioned_price
            order.save(update_fields=['discounted_price'])
            data = {
                'detail':'promo kod muvaffaqiyatli qo\'llandi',
                'original_price':price,
                'promotioned_price':promotioned_price,
                'discount_percent':int(promotion['interest']),
            }
            
            UserUsedPromotion.objects.create(
                user=request.user,
                promotion_id=promotion['id'],
                promotion_type=promotion['type']
            )
            return Response(data, status=200)
        return Response({'detail':'promo kod ishlamadi'}, status=200)    



class OrderDetailView(ListAPIView):
    permission_classes = [p.IsAuthenticated]
    serializer_class = OrderSerializer

    def get(self, request, order_id, *args, **kwargs):
        order = Order.objects.get(id=order_id)
        if order.status == Order.OrderStatus.CANCELED or order.status == Order.OrderStatus.DELIVERED or order.status == Order.OrderStatus.IS_PAID:
            return Response({'detail': 'bu order uchun payment qilaolmaysiz'}, status=400)
        serializer = self.serializer_class(order, many=False)
        return Response(serializer.data, status=200)
    
    
class CreatePaymentView(APIView):
    permission_classes = [p.IsAuthenticated]
    serializer_class = PaymentCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = PaymentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_id = serializer.validated_data['order_id']
        provider = serializer.validated_data['provider']
        
        
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return Response({'detail': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        if order.status == Order.OrderStatus.IS_PAID:
            return Response({'detail':'bu order allaqachin tulangan' }, status=400)
        if order.status == Order.OrderStatus.CANCELED:
            return Response({'detail':'bu order allaqachin bekor qilingan' }, status=400)
        
        try:
            check = Payment.objects.filter(order=order).first()
            
        except Payment.DoesNotExist:
            pass
        
        
        if check:
                if check.status == Payment.PaymentProvider.ON_DELIVERY:
                    return Response({'detail':'bu maxsulot on delivery da'})
        if order.taker is None:
            return Response({'detail': 'Productlarni qabul qilib luvchi qushing'}, status=status.HTTP_400_BAD_REQUEST)
        
        if order.user != request.user:
            return Response({'detail': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)
        procider_id = PaymentService.create_provider_id()

        payment = PaymentService.create_payment_for_order(order, provider, procider_id)
        if payment['result']['provider'] == 'on_delivery':
            return Response({'detail':'mijozga yetkazib berish punkti uchun payment yaratildi', 'payment': payment}, status=status.HTTP_201_CREATED)
        
        send_verification_link.delay(request.user.id, payment['result']['id'])
        return Response({'detail':'email ingizga tasdiqlash havolasi yuborildi', 'payment': payment}, status=status.HTTP_201_CREATED)


class PaymentCallbackView(APIView):

    def get(self, request, *args, **kwargs):
        token = request.query_params.get('token')
        payment_id = request.query_params.get('payment_id')
        if not payment_id:
            return Response({'detail':'payment_id kelmadi'}, status=400)
        if not token:
            return Response({'detail':'token kelmadi'}, status=400)
        
        user_id = verify_verification_token(token)
        if not user_id:
            return Response({'detail':'token notogri yoki muddati utgan'}, status=400)
        
        payment = PaymentService.handle_provider_callback(payment_id, status='success')
        
        return Response({'detail':'payment muvaffaqiyatli verifikatsiya qilindi', 'payment_status':payment.status}, status=200)




    
    