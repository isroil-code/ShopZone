from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:pk>/product/', views.AddToCart.as_view(), name='add-to-card'),
    path('delete/<int:pk>/product/', views.DeleteFromCart.as_view(), name='delete-from-cart'),
    path('increase/<int:pk>/quantity/', views.IncreaseQuantityView.as_view(), name='increase quantity'),
    path('decrease/<int:pk>/quantity/', views.DecreaseQuantityView.as_view(), name='decrease quantity'),
    path('select/<int:pk>/product/', views.SelectCartItemView.as_view(), name='select_cart_item'),
    path('', views.CartView.as_view(), name='cart_view'),
    
    path('add/<int:pk>/wishlist/', views.AddToWishlist.as_view(), name='add_to_wishlist'),
    path('delete/<int:pk>/wishlist/', views.DeleteFromWishlist.as_view(), name='delete_from_wishlist'),
    path('wishlist/', views.WishlistView.as_view(), name='wishlist')
]