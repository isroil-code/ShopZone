from django.db import router
from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'seller/products', views.ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('product-list/', views.ProductsView.as_view(), name='product-list'),
    path('product-detail/<int:id>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('category/<int:category_id>/products/', views.ProductCategoryView.as_view(), name='products-by-category')  ,
    path('seller/product-create/', views.CreateProductView.as_view(), name='product-create'),
    
    path('product/<int:pk>/approve', views.ProductApprove.as_view(), name='product_approve'),
    path('product/<int:pk>/reject', views.ProductReject.as_view(), name='product_reject'),
    
]

