from django.shortcuts import get_object_or_404, render
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView
from rest_framework import permissions as p

from apps_.sellers.models import Seller
from django_filters import rest_framework as filters
from .serializers import (ProductSerializer, ProductDetailSerializer, ProductImageSerializer,ProductVideosSerializer, ProductCreateSerializer,
                          ProductSertificateSerializer, ProductInstructionSerializer, ProductPriceSerializer, ProductStockSerializer, MadeCountrySerializer)
from .services import get_or_create_product
from rest_framework.response import Response
from .models import Product
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from log.utils import log_activity
from .filters import ProductFilter

def get_draft_product(self ,pk):
    return get_object_or_404(
        Product,
        pk=pk,
        seller=self.request.user.seller,
        status=Product.Status.DRAFT
    )
    

    

class CreateProductView(CreateAPIView):
    permission_classes = [p.IsAuthenticated]
    serializer_class = ProductCreateSerializer

    def perform_create(self, serializer):
        seller = get_object_or_404(Seller, user=self.request.user)
        serializer.save(seller=seller)
        


class ProductViewSet(ModelViewSet):
    permission_classes = [p.IsAuthenticated]
    serializer_class = ProductSerializer
    http_method_names = ['get', 'post', 'put', 'patch',]

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user.seller)


    def get(self, request, *args, **kwargs):
        serialzier = ProductSerializer(self.get_queryset(), many=True)
        return Response(serialzier.data)
       
    
    @action(detail=True, methods=['post'], serializer_class=ProductDetailSerializer)
    def add_detail(self, request,pk=None, *args, **kwargs):
        product = get_draft_product(self, pk)
        serializer = self.get_serializer(data=request.data)     
        serializer.is_valid(raise_exception=True)
        serializer.save(product=product)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], serializer_class=ProductImageSerializer)
    def add_image(self, request,pk=None, *args, **kwargs):
        product = get_draft_product(self, pk)
        serializer = ProductImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(product=product)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], serializer_class=ProductVideosSerializer)
    def add_video(self, request,pk=None, *args, **kwargs):
        product = get_draft_product(self, pk)
        serializer = ProductVideosSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(product=product)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], serializer_class=ProductSertificateSerializer)
    def add_sertificate(self, request,pk=None, *args, **kwargs):
        product = get_draft_product(self, pk)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(product=product)
        return Response(serializer.data)
    
    
    
    @action(detail=True, methods=['post'], serializer_class=ProductInstructionSerializer)
    def add_instruction(self, request,pk=None, *args, **kwargs):
        product = get_draft_product(self, pk)
        serializer = ProductInstructionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(product=product)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], serializer_class=ProductPriceSerializer)
    def add_price(self, request,pk=None, *args, **kwargs):
        product = get_draft_product(self, pk)
        serializer = ProductPriceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(product=product)
        return Response(serializer.data)
    
    
    @action(detail=True, methods=['post'], serializer_class=ProductStockSerializer)
    def add_stock(self, request,pk=None, *args, **kwargs):
        product = get_draft_product(self, pk)
        serializer = ProductStockSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(product=product)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], serializer_class=ProductSerializer)
    def finalize_product(self, request,pk=None, *args, **kwargs):
        product = get_draft_product(self, pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

    
class ProductsView(ListAPIView):
    permission_classes = [p.AllowAny]
    authentication_classes = []
    serializer_class = ProductSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProductFilter    
    queryset = Product.objects.all()


class ProductDetailView(GenericAPIView):
    permission_classes = [p.AllowAny]
    authentication_classes = []
    serializer_class = ProductSerializer
    
    def get(self, request, id):
        
        product = get_object_or_404(Product, id=id)
        serializer = self.serializer_class(product, context={'request': request})
        return Response(serializer.data)
    
   
    
    

