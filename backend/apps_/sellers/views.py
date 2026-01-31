from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import permissions as p
from .serializers import SellerSerializer, SellerProfileSerializer, SellerIndividualSerializer, SellerEntrepreneurSerializer, SellerCompanySerializer, SellerInformationSerializer, BankAccountSerializer, SellerCommisionerSerializer
from rest_framework.response import Response
from .models import Seller, SellerProfile, Shartnoma
from drf_spectacular.utils import extend_schema, OpenApiResponse, PolymorphicProxySerializer
from rest_framework import serializers
from django.db import transaction
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .services import create_shartnoma, create_seller_balnce

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
        
class SellerProfileCreateView(GenericAPIView):
    permission_classes = [p.IsAuthenticated]
    serializer_class = SellerProfileSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        check_profile = SellerProfile.objects.filter(seller__user=request.user).first()
        if check_profile:
            return Response({"detail": "Seller profile already exists for this user."}, status=400) 
        
        seller = Seller.objects.get(user=request.user)
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
            biznes_type = seller.biznes_type
            if biznes_type == 'individual':
                return SellerIndividualSerializer
            elif biznes_type == 'entrepreneur':
                return SellerEntrepreneurSerializer
            elif biznes_type == 'company':
                return SellerCompanySerializer
            else:
                raise serializers.ValidationError("Invalid biznes_type")
        except Seller.DoesNotExist:
            raise serializers.ValidationError("Seller not found")
    
    @transaction.atomic 
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        seller = Seller.objects.get(user=request.user)
        serializer.save(seller=seller)
        return Response(serializer.data, status=201)

class SellerBankAccountView(GenericAPIView):
    permission_classes = [p.IsAuthenticated]
    serializer_class = BankAccountSerializer
    
    def post(self, request, *args, **kwargs):
        serialzier = self.serializer_class(data=request.data)
        serialzier.is_valid(raise_exception=True)
        
        seller = Seller.objects.filter(user=self.request.user).first()
        serialzier.save(seller=seller)
        create_shartnoma(seller)
        create_seller_balnce(seller)
        return Response({'detail':'User Bank Account info taken'}, status=status.HTTP_200_OK)


class SellerCommisionerView(GenericAPIView):
    serializer_class = SellerCommisionerSerializer

    def get(self, request, *args, **kwargs):
        seller = Seller.objects.filter(user=self.request.user).first()
        serializer = self.serializer_class(seller)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)   
        shartnoma = Shartnoma.objects.filter(seller__user=self.request.user).first()
        if shartnoma:   
            shartnoma.tasdiqlash_screenshoti_or_rasmi = serializer.validated_data.get('tasdiqlash_screenshoti_or_rasmi')
            shartnoma.save()
            return Response({'detail':'Shartnoma tasdiqlash screenshoti yoki rasmi muvaffaqiyatli yuklandi'}, status=status.HTTP_200_OK)
        return Response({'detail':'Shartnoma topilmadi'}, status=status.HTTP_404_NOT_FOUND)

class AdminSellerInfoView(ModelViewSet):
    # permission_classes = [p.IsAdminUser]
    serializer_class = SellerInformationSerializer
    queryset = Seller.objects.all()
    http_method_names = ['get', 'list', 'put', 'patch']
    
    
    
