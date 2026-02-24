from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"admin-category", views.CategoryAdminView, basename='admin_category')


urlpatterns = [
    path('categories-list/', views.CategoryView.as_view(),name='categories'),
    path('categories/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('api/',include(router.urls))
]