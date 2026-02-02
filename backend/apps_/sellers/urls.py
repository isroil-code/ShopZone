from django.urls import include, path
from .views import AdminSellerInfoView, SellerCommisionerView, SellerCreateView, SellerBusinessTypeUpdateView, SellerProfileCreateView, SellerTakeInfoView, SellerBankAccountView, SellerOnboardingStatusView , DeleteSellerActionView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'sellers', AdminSellerInfoView, basename='admin-seller-info')    



urlpatterns = [
    path('become/seller/', SellerCreateView.as_view(), name='seller-create'),  
    path('business-type/', SellerBusinessTypeUpdateView.as_view(), name='seller-business-type-update'),
    path('profile/create/', SellerProfileCreateView.as_view(), name='seller-profile-create'),
    path('requisites/', SellerTakeInfoView.as_view(), name='seller-info-take'),
    path('bank/account/',SellerBankAccountView.as_view(), name='seller-bank-account'),
    path('commissioner/',SellerCommisionerView.as_view(), name='seller-commissioner'),
    path('onboarding/status/', SellerOnboardingStatusView.as_view(), name='seller-onboarding-status'),
    path('admin/', include(router.urls), name='admin-seller-info'),
    
    path('delete/seller/action/', DeleteSellerActionView.as_view(), name='seller-action-view')
]






