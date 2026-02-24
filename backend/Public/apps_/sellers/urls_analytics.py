from django.urls import path
from .views_analytics import SellerAnalyticsView

urlpatterns = [
    path('seller/', SellerAnalyticsView.as_view(), name='seller-analytics'),
]
