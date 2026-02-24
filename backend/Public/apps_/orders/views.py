from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import permissions as p
from apps_.users import serializer
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from rest_framework.response import Response
from apps_.cart.models import Cart, CartItem
from .services import OrderService

class CreateOrderView(GenericAPIView):
    permission_classes = [p.IsAuthenticated]
  
    
    def post(self, request, *args, **kwargs):
        user = self.request.user
        cart = Cart.objects.filter(user=user).first()
        if not cart.items.exists():
            return Response({'detail':'Cart da hech narsa yuq'}, status=400)
        
        order_service = OrderService()
        order = order_service.order_create(cart, request) 
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=201)


class CancelOrderView(GenericAPIView):
    permission_classes = [p.IsAuthenticated]
    
    
    def post(self, request, pk, *args, **kwargs):
        user = self.request.user
        order = Order.objects.filter(user=user, id=pk).first()
        if not order:
            return Response({'detail':'Bunday order mavjud emas'}, status=404)
        
        order_service = OrderService()
        order_service.order_cancel(order)
        return Response({'status':'cancelled'}, status=200)
    


class MyOrdersView(GenericAPIView):
    permission_classes = [p.IsAuthenticated]
    serializer_class = OrderSerializer
    
    def get(self, request, *args, **kwargs):
        user = self.request.user
        orders = Order.objects.filter(user=user)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data, status=200)
    
    
