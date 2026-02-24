from django.shortcuts import render
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework import permissions as p

from .models import Review


from .serializers import ReviewCreateSerializer, ReviewListSerializer
from apps_.products.models import Product
from rest_framework.response import Response
from config.pagination import CustomPagination
from apps_.orders.models import OrderItem

class ReviewCreateView(GenericAPIView):
    permission_classes = [p.IsAuthenticated]
    serializer_class = ReviewCreateSerializer
    
    def post(self, request,pk=None, *args, **kwargs):
        product = Product.objects.get(pk=pk)
        
        checking = OrderItem.objects.filter(order__user=request.user, product=product, order__status='delivered').exists()
        
        if not checking:
            return Response({'error': 'birinchi sotib oling'}, status=400)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        product = Product.objects.get(pk=pk)
        serializer.save(user=request.user, product=product)
        return Response(serializer.data, status=201)

class ReviewListByProduct(ListAPIView):
    permission_classes = [p.IsAuthenticated]
    serializer_class = ReviewListSerializer
    pagination_class = CustomPagination
    
    def get_queryset(self):
        product_id = self.kwargs.get('pk')
        return Review.objects.filter(product_id=product_id).order_by('-created_at')
    
    