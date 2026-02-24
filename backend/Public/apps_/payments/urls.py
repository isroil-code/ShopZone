from django.urls import path
from .views import CreatePaymentView, GetPromotionCodeView, PaymentCallbackView, CreateTakerView, CreateTopshirishPunktView, OrderDetailView

urlpatterns = [
    path('get/<int:order_id>/', OrderDetailView.as_view(), name='order-detail'),
    path('create/', CreatePaymentView.as_view(), name='payment-create'),
    path('callback/', PaymentCallbackView.as_view(), name='payment-callback'),
    path('taker/create/<int:order_id>/', CreateTakerView.as_view(), name='create-taker'),
    path('topshirish-punkt/create/<int:order_id>/', CreateTopshirishPunktView.as_view(), name='create-topshirish-punkt'),
    path('promotion-code/<int:order_id>/<str:code>/', GetPromotionCodeView.as_view(), name='get-promotion-code'),
]
