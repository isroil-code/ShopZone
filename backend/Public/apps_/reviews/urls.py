from django.urls import path
from . import views


urlpatterns = [
    path('add/<int:pk>/product/', views.ReviewCreateView.as_view(), name='add-review'),
    path('<int:pk>/review/', views.ReviewListByProduct.as_view(), name='review-detail'),
]

    