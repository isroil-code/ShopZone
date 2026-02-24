from django.urls import include, path
from .views import AdminSellerInfoView, SellerBalanceView, SellerCommisionerView, SellerCreateView, SellerBusinessTypeUpdateView, SellerProfileCreateView, SellerTakeInfoView, SellerBankAccountView, MyProductsSellerView
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
    path('admin/', include(router.urls), name='admin-seller-info'),
    
    path('balance/', SellerBalanceView.as_view(), name='seller-balance'),
    path('my-products/',MyProductsSellerView.as_view(), name='my_products' )
    
]






