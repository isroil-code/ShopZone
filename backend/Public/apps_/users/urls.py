from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"users", views.UsersListAdmin, basename='users_admin')

urlpatterns = [
    path('login/', views.LoginView.as_view(),name='login_view'),
    path('verify-email/', views.VerifyView.as_view(), name='verify_otp'),
    path('settings/', views.UserProfileView.as_view(), name='settings'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password/forgot/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('password/verify-otp/', views.VerifyRecoveryOtpView.as_view(),name='recovery_otp'), 
    path('password/reset/', views.SetPasswordView.as_view(), name='set_password'), 
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('admin/', include(router.urls))
]

