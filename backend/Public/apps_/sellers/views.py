from rest_framework import serializers


from django.shortcuts import render
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework import permissions as p
from .serializers import SellerSerializer, SellerProfileSerializer, SellerIndividualSerializer, SellerEntrepreneurSerializer, SellerCompanySerializer, SellerInformationSerializer, BankAccountSerializer, SellerCommisionerSerializer
from rest_framework.response import Response
from .models import Seller, SellerProfile, Shartnoma, SellerBalance, SellerBankAccount, SellerCompany, SellerEntrepreneur, SellerIndividual
from drf_spectacular.utils import extend_schema, OpenApiResponse, PolymorphicProxySerializer
from rest_framework import serializers
from django.db import transaction
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .services import create_shartnoma, create_seller_balnce
from rest_framework.views import APIView
from config.permissions import IsSeller, IsAdmin
from rest_framework.decorators import action
from apps_.products.models import Product
from apps_.products.serializers import ProductDetailSerializer, ProductSerialzer
from apps_.products.services import ProductDetailService
from config.pagination import CustomPagination
from apps_.products.filters import ProductFilter
from django_filters import rest_framework as filters





class SellerCreateView(GenericAPIView):
    permission_classes = [p.IsAuthenticated]
    serializer_class = SellerSerializer
    
    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        check_seller = Seller.objects.filter(user=request.user).first()
        if check_seller:
            return Response({"detail": "Seller already exists for this user."}, status=400)
        
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)

class SellerBusinessTypeUpdateView(GenericAPIView):
    permission_classes = [p.IsAuthenticated]
    serializer_class = SellerSerializer
    
    @transaction.atomic
    def patch(self, request, *args, **kwargs):
        seller = Seller.objects.filter(user=request.user).first()
        
        if not seller:
            return Response({"detail": "Seller topilmadi."}, status=404)
        
        biznes_type = request.data.get('biznes_type')
        if not biznes_type:
            return Response({"detail": "biznes_type majburiy."}, status=400)
        
        if biznes_type not in ['individual', 'entrepreneur', 'company']:
            return Response({"detail": "Noto'g'ri biznes_type."}, status=400)
        
      
        if seller.biznes_type and seller.biznes_type != biznes_type:
           
            if seller.biznes_type == 'individual' and hasattr(seller, 'individual_info'):
                seller.individual_info.delete()
            elif seller.biznes_type == 'entrepreneur' and hasattr(seller, 'entrepreneur_info'):
                seller.entrepreneur_info.delete()
            elif seller.biznes_type == 'company' and hasattr(seller, 'company_info'):
                seller.company_info.delete()
        
        seller.biznes_type = biznes_type
        seller.save()
        
        serializer = self.get_serializer(seller)
        return Response(serializer.data, status=200)
        
class SellerProfileCreateView(GenericAPIView):
    permission_classes = [p.IsAuthenticated]
    serializer_class = SellerProfileSerializer
    
    def post(self, request, *args, **kwargs):
        seller = Seller.objects.filter(user=request.user).first()
        if not seller:
            return Response({"detail": "Seller topilmadi. Avval seller yarating."}, status=404)
       
        existing_profile = SellerProfile.objects.filter(seller=seller).first()
        
        if existing_profile:
            serializer = self.get_serializer(existing_profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=200)
 
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(seller=seller)
        return Response(serializer.data, status=201)



@extend_schema(
    request=PolymorphicProxySerializer(
        component_name="SellerRequisites",
        serializers=[
            SellerIndividualSerializer,
            SellerEntrepreneurSerializer,
            SellerCompanySerializer,
        ],
        resource_type_field_name="biznes_type",
    ),
    responses={201: None}
)
class SellerTakeInfoView(GenericAPIView):
    permission_classes = [p.IsAuthenticated]
  
    def get_serializer_class(self):
        user = self.request.user
        try:
            seller = Seller.objects.filter(user=user).first()
            if not seller:
                raise serializers.ValidationError("Seller topilmadi")
            
            biznes_type = seller.biznes_type
            if not biznes_type:
                raise serializers.ValidationError("Biznes turi tanlanmagan. Avval biznes turini tanlang.")
            
            if biznes_type == 'individual':
                return SellerIndividualSerializer
            elif biznes_type == 'entrepreneur':
                return SellerEntrepreneurSerializer
            elif biznes_type == 'company':
                return SellerCompanySerializer
            else:
                raise serializers.ValidationError("Noto'g'ri biznes_type")
        except Seller.DoesNotExist:
            raise serializers.ValidationError("Seller topilmadi")
    
    @transaction.atomic 
    def post(self, request, *args, **kwargs):
        seller = Seller.objects.filter(user=request.user).first()
        if not seller:
            return Response({"detail": "Seller topilmadi."}, status=404)
        
        if not seller.biznes_type:
            return Response({"detail": "Biznes turi tanlanmagan."}, status=400)
        
      
        existing_requisite = None
        if seller.biznes_type == 'individual':
            existing_requisite = SellerIndividual.objects.filter(seller=seller).first()
        elif seller.biznes_type == 'entrepreneur':
            existing_requisite = SellerEntrepreneur.objects.filter(seller=seller).first()
        elif seller.biznes_type == 'company':
            existing_requisite = SellerCompany.objects.filter(seller=seller).first()
        
        if existing_requisite:
            serializer = self.get_serializer(existing_requisite, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=200)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(seller=seller)
        return Response(serializer.data, status=201)

class SellerBankAccountView(GenericAPIView):
    permission_classes = [p.IsAuthenticated]
    serializer_class = BankAccountSerializer
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        seller = Seller.objects.filter(user=request.user).first()
        if not seller:
            return Response({'detail': 'Seller topilmadi.'}, status=status.HTTP_404_NOT_FOUND)
        
      
        existing_bank_account = SellerBankAccount.objects.filter(seller=seller).first()
        
        if existing_bank_account:
            serializer = self.serializer_class(existing_bank_account, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
      
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(seller=seller)
        

        if not Shartnoma.objects.filter(seller=seller).exists():
            create_shartnoma(seller)
        
        if not SellerBalance.objects.filter(seller=seller).exists():
            create_seller_balnce(seller)
        
        return Response({'detail': 'Bank account ma\'lumotlari saqlandi'}, status=status.HTTP_200_OK)


class SellerCommisionerView(GenericAPIView):
    permission_classes = [p.IsAuthenticated] 
    serializer_class = SellerCommisionerSerializer

    def get(self, request, *args, **kwargs):
        seller = Seller.objects.filter(user=request.user).first()
        if not seller:
            return Response({'detail': 'Seller topilmadi.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(seller)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)   
        shartnoma = Shartnoma.objects.filter(seller__user=request.user).first()
        if shartnoma:   
            shartnoma.tasdiqlash_screenshoti_or_rasmi = serializer.validated_data.get('tasdiqlash_screenshoti_or_rasmi')
            shartnoma.save()
            return Response({'detail':'Shartnoma tasdiqlash screenshoti yoki rasmi muvaffaqiyatli yuklandi'}, status=status.HTTP_200_OK)
        return Response({'detail':'Shartnoma topilmadi'}, status=status.HTTP_404_NOT_FOUND)


class SellerBalanceView(GenericAPIView):
    permission_classes = [IsSeller] 

    def get(self, request, *args, **kwargs):
        seller = Seller.objects.filter(user=request.user).first()
        if not seller:
            return Response({'detail': 'Seller topilmadi.'}, status=status.HTTP_404_NOT_FOUND)
        try:
            balance = SellerBalance.objects.filter(seller=seller).first()
        except SellerBalance.DoesNotExist:
            return Response({'detail':'balance yuq'}, status=404)
        
        if not balance:
            return Response({'detail': 'Seller balance topilmadi.'}, status=status.HTTP_404_NOT_FOUND)
        
        data = {
            'balance': balance.amount,
            'last_updated': balance.updated_at
        }
        return Response(data, status=status.HTTP_200_OK)

class MyProductsSellerView(ListAPIView):
    permission_classes = [IsSeller]
    serializer_class = ProductSerialzer
    pagination_class = CustomPagination
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProductFilter    
    
    
    
    def get_queryset(self):
        seller = Seller.objects.filter(user=self.request.user).first()
        if not seller:
            return Product.objects.none()
        return Product.objects.filter(seller=seller)
    
    

            
            
        

class AdminSellerInfoView(ModelViewSet):
    permission_classes = [IsAdmin] 
    serializer_class = SellerInformationSerializer
    queryset = Seller.objects.all()
    http_method_names = ['get', 'list', 'put', 'patch', 'post']
    
    @action(detail=True, methods=['post'], serializer_class=None)
    def approve_seller(self, request, pk=None, *args, **kwargs):
        try:
            seller = Seller.objects.get(pk=pk)
        except Seller.DoesNotExist:
            return Response({'detail': 'Seller topilmadi.'}, status=404)
        shartnoma = Shartnoma.objects.filter(seller=seller).first()
        if not shartnoma or not shartnoma.tasdiqlash_screenshoti_or_rasmi:
            return Response({'detail': 'Sellerning shartnomasi yoki tasdiqlash screenshoti/rasmi topilmadi.'}, status=status.HTTP_400_BAD_REQUEST)
        seller.status = 'verified'
        seller.user.role = 'seller'
        seller.user.save(update_fields=['role'])
        seller.save(update_fields=['status'])
        return Response({'detail': 'Seller muvaffaqiyatli tasdiqlandi.'}, status=status.HTTP_200_OK)


    @action(detail=True, methods=['post'], serializer_class=None)
    def reject_seller(self, request, pk=None, *args, **kwargs):
        try:
            seller = Seller.objects.get(pk=pk)
        except Seller.DoesNotExist:
            return Response({'detail':'seller topilmadi'}, status=404)
        if not seller:
            return Response({'detail':'seller kelmadi'})
        seller.status = 'rejected'
        seller.save(update_fields=['status'])
        return Response({'detail': 'Seller tasdiqlanmadi.'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], serializer_class=None)
    def block_seller(self, request, pk=None, *args, **kwargs):
        try:
            seller = Seller.objects.get(pk=pk)
        except Seller.DoesNotExist:
            return Response({'detail':'seller topilmadi'}, status=404)
        if not seller:
            return Response({'detail':'seller kelmadi'})
        seller.status = 'blocked'
        seller.save(update_fields=['status'])
        return Response({'detail': 'Seller bloklandi.'}, status=status.HTTP_200_OK)
    

