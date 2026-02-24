from rest_framework import generics
from .serializers import PromotionToSellerSerializer, PromotionToProductSerializer
from .models import PromotionToSeller, PromotionToProduct
from config.permissions import IsSellerOrAdmin


class PromotionToSellerCreateView(generics.CreateAPIView):
    permission_classes = [IsSellerOrAdmin]
    queryset = PromotionToSeller.objects.all()
    serializer_class = PromotionToSellerSerializer

class PromotionToProductCreateView(generics.CreateAPIView):
    permission_classes = [IsSellerOrAdmin]
    queryset = PromotionToProduct.objects.all()
    serializer_class = PromotionToProductSerializer
    
class PromotionsProductListView(generics.ListAPIView):
    permission_classes = [IsSellerOrAdmin]
    queryset = PromotionToProduct.objects.all()
    serializer_class = PromotionToProductSerializer
    
class PromotionsSellerListView(generics.ListAPIView):
    permission_classes = [IsSellerOrAdmin]
    queryset = PromotionToSeller.objects.all()
    serializer_class = PromotionToSellerSerializer
    