from django.shortcuts import render
from rest_framework.generics import GenericAPIView
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

class SellerCreateView(GenericAPIView):
    permission_classes = [p.IsAuthenticated]
    serializer_class = SellerSerializer
    
    def post(self, request, *args, **kwargs):
        # Allow creating Seller without biznes_type initially
        # biznes_type will be set in Step 1 via PATCH
        data = request.data.copy() if request.data else {}
        
        # Remove biznes_type from initial creation if present
        # It will be set via separate endpoint
        if 'biznes_type' in data:
            del data['biznes_type']
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        check_seller = Seller.objects.filter(user=request.user).first()
        if check_seller:
            return Response({"detail": "Seller already exists for this user."}, status=400)
        
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)

class SellerBusinessTypeUpdateView(GenericAPIView):
    permission_classes = [p.IsAuthenticated]
    serializer_class = SellerSerializer
    
    def patch(self, request, *args, **kwargs):
        seller = Seller.objects.filter(user=request.user).first()
        
        if not seller:
            return Response({"detail": "Seller not found for this user."}, status=404)
        
        if seller.biznes_type is not None:
            return Response({"detail": "Business type already set."}, status=400)
        
        biznes_type = request.data.get('biznes_type')
        if not biznes_type:
            return Response({"detail": "biznes_type is required."}, status=400)
        
        if biznes_type not in ['individual', 'entrepreneur', 'company']:
            return Response({"detail": "Invalid biznes_type."}, status=400)
        
        seller.biznes_type = biznes_type
        seller.save()
        
        serializer = self.get_serializer(seller)
        return Response(serializer.data, status=200)
        
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
        print(serializer)
        serializer.is_valid(raise_exception=True)
        print(serializer)
 
        
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

class SellerOnboardingStatusView(APIView):
    permission_classes = [p.IsAuthenticated]

    def get(self, request):
        seller = Seller.objects.filter(user=request.user).first()

        if not seller:
            return Response({
                "seller_exists": False,
                "current_step": 1
            })

        steps = {
            1: seller.biznes_type is not None,
            2: hasattr(seller, 'profile'),
            3: hasattr(seller, 'requisites'),
            4: hasattr(seller, 'bank_account'),
            5: hasattr(seller, 'commissioner'),
        }

        current_step = next(
            (step for step, done in steps.items() if not done),
            6
        )

        return Response({
            "seller_exists": True,
            "current_step": current_step,
            "onboarding_completed": current_step > 5
        })


class DeleteSellerActionView(GenericAPIView):
    permission_classes = [p.IsAuthenticated]
    
    def delete(self, request, *args, **kwargs):
        seller = request.user.seller
        try:
            if seller.profile:
                profile = SellerProfile.objects.get(seller=seller)
                profile.delete()
            elif seller.individual_info:
                data = SellerIndividual.objects.get(seller=seller)
                data.delete()
            elif seller.entrepreneur_info:
                data = SellerEntrepreneur.objects.get(seller=seller)
                data.delete()
            elif seller.company_info:
                data = SellerCompany.objects.get(seller=seller)
                data.delete()
            elif seller.bank_account:
                data = SellerBankAccount.objects.get(seller=seller)
                data.delete()
            elif seller.shartnoma:
                data = Shartnoma.objects.get(seller=seller)
                data.delete()
            elif seller.balance:
                data = SellerBalance.objects.get(seller=seller)
                data.delete()
            return Response({'datail':'seller malumotlari saqlanmadi'}, status=200)
        except:
            return Response({'datail':'nimadir notugri ketti'}, status=400)

class AdminSellerInfoView(ModelViewSet):
    # permission_classes = [p.IsAdminUser]
    serializer_class = SellerInformationSerializer
    queryset = Seller.objects.all()
    http_method_names = ['get', 'list', 'put', 'patch']

    
    

