from django.shortcuts import get_object_or_404, render
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView
from rest_framework import permissions as p

from apps_.sellers.models import Seller
from django_filters import rest_framework as filters

from apps_.categories.models import Category
from apps_.categories.services import CategoryService
from apps_.categories.serializers import CategorySerializer

from .serializers import (ProductSerialzer, ProductDetailSerializer, ProductImageSerializer,ProductVideosSerializer, ProductCreateSerializer,
                          ProductSertificateSerializer, ProductInstructionSerializer, ProductPriceSerializer, ProductStockSerializer, ProductDetailsSerializer)
from .services import get_or_create_product
from rest_framework.response import Response
from .models import Product
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from .filters import ProductFilter
from .services import ProductDetailService
from config.pagination import CustomPagination
from django.utils import timezone
from django.db.models import Sum, Count
from config.permissions import IsSellerOrAdmin, IsAdmin
from django.conf import settings




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
    permission_classes = [IsSellerOrAdmin]  
    serializer_class = ProductSerialzer
    http_method_names = ['get', 'post', 'put', 'patch',]

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user.seller)


    def get(self, request, *args, **kwargs):
        serialzier = ProductSerialzer(self.get_queryset(), many=True)
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
    
class ProductApprove(GenericAPIView):
    permission_classes = [IsAdmin]
    queryset = Product.objects.all()
    
    def post(self, request,pk=None, *args, **kwargs):
        product = self.get_object()
        product.status = Product.Status.APPROVED
        product.save(update_fields=['status'])
        return Response({'detail':'done, product approved'}, status=200)
    
    
    
class ProductReject(GenericAPIView):
    permission_classes = [IsAdmin]
    queryset = Product.objects.all()
    
    def post(self, request,pk=None, *args, **kwargs):
        product = self.get_object()
        product.status = Product.Status.REJECTED
        product.save(update_fields=['status'])
        return Response({'detail':'done, product approved'}, status=200)
    
        
    
    
class ProductsView(ListAPIView):
    permission_classes = [p.AllowAny]
    serializer_class = ProductSerialzer
    filter_backends = [filters.DjangoFilterBackend]
    queryset = Product.objects.all()
    pagination_class = CustomPagination
    
    
    def get(self, request, *args, **kwargs):
        print(settings.NGROK_URL)
        week_ago = timezone.now() - timezone.timedelta(days=7)
        
        sold_products = Product.objects.filter(
            status=Product.Status.APPROVED,
            orders__order__order_date__gte=week_ago
        ).annotate(
            total_sold=Sum('orders__quantity')
        ).order_by('-total_sold')[:10]

    
        reviewed_products = Product.objects.filter(
            status=Product.Status.APPROVED,
            reviews__created_at__gte=week_ago
        ).annotate(
            review_count=Count('reviews')
        ).order_by('-review_count')[:10]

        weekly_products = list(sold_products) + [p for p in reviewed_products if p not in sold_products]
        weekly_products = weekly_products[:20]
        weekly_data = self.get_serializer(weekly_products, many=True).data

        all_products = Product.objects.filter(status=Product.Status.APPROVED).order_by('-created_at')
        page = self.paginate_queryset(all_products)
        if page is not None:
            all_products_data = self.get_serializer(page, many=True).data
            return self.get_paginated_response({
                'weekly_products': weekly_data,
                'products': all_products_data
            })
        all_products_data = self.get_serializer(all_products, many=True).data
        return Response({
            'weekly_products': weekly_data,
            'products': all_products_data
        })
    
class ProductCategoryView(ListAPIView):
    permission_classes = [p.AllowAny]
    serializer_class = ProductSerialzer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProductFilter    
    queryset = Product.objects.all()
    pagination_class = CustomPagination
    
    def get(self, request, category_id, *args, **kwargs):
        category = get_object_or_404(Category, id=category_id)
        category_data = CategorySerializer(category).data

        try:
            category_ids = CategoryService.get_category_and_children_ids(category)
        except Exception:
            category_ids = [category.id]

        base_qs = self.get_queryset().filter(category_id__in=category_ids)
        filtered_qs = self.filter_queryset(base_qs)

        page = self.paginate_queryset(filtered_qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'category': category_data,
                'products': serializer.data
            })

        serializer = self.get_serializer(filtered_qs, many=True)
        return Response({
            'category': category_data,
            'products': serializer.data
        })

class ProductDetailView(GenericAPIView):
    permission_classes = [p.AllowAny]
    serializer_class = ProductDetailsSerializer
    
    def get(self, request, id):
        product = get_object_or_404(Product, id=id)
        user = self.request.user
        request = self.request
        detail = ProductDetailService.get_details(product, user, request)
        serializer = self.serializer_class(detail, context={'request': request})
        return Response(serializer.data)
        
    
   
    
    

