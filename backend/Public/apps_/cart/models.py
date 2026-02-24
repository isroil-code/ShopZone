from django.db import models
from apps_.users.models import User
from apps_.products.models import Product

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='card')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.email

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_product')
    quantity = models.IntegerField(default=1)
    is_selected = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.cart.user.email} - cart item"
    
    
class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlist')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.email
    
class WishlistItems(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name='wishlist_products')
    
    def __str__(self):
        return self.wishlist.user.email 
    