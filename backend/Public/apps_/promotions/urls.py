from django.urls import path
from . import views



urlpatterns = [
    path('create/seller/', views.PromotionToSellerCreateView.as_view(), name='promotion-to-seller-create'),
    path('create/product/', views.PromotionToProductCreateView.as_view(), name='promotion-to-product-create'),
    path('list/seller/', views.PromotionsSellerListView.as_view(), name='promotion-to-seller-list'),
    path('list/product/', views.PromotionsProductListView.as_view(), name='promotion-to-product-list'),
    
]