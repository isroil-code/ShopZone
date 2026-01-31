from django.shortcuts import render
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView
from rest_framework import permissions as p

from apps_.sellers.models import Seller
from .serializers import ProductSerializer, ProductDetailSerializer, ProductMediaSerializer, ProductCreateSerializer, ProductSertificateSerializer
from .services import get_or_create_product
from rest_framework.response import Response
from .models import Product
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action


class ProductCreateView(CreateAPIView):
    permission_classes = [p.IsAuthenticated]
    serializer_class = ProductCreateSerializer

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user.seller)

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=['post'], serializer_class=ProductDetailSerializer)
    def add_detail(self, request, *args, **kwargs):
        product = get_or_create_product(request.user.seller)
        serializer = ProductDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(product=product)
        return Response(serializer.data)

class ProductsView(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    