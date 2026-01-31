from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter




urlpatterns = [
    path('create/', views.ProductCreateView.as_view(), name='product-create'),
    
]

