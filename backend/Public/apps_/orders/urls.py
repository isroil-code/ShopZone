from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CreateOrderView.as_view(), name='order-create'),  
    path('<int:pk>/cancel/', views.CancelOrderView.as_view(), name='order-cancel'),
    path('my-orders/', views.MyOrdersView.as_view(), name='my-orders'),
]

