from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterSellerView.as_view(), name='register-seller'),
    path('login/', views.LoginSellerView.as_view(), name='login-seller'),
    path('verify/', views.VerifySellerView.as_view(), name='verify-seller'),
]