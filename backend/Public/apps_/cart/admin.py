from django.contrib import admin
from .models import Cart, CartItem, Wishlist, WishlistItems

admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(WishlistItems)
# Register your models here.
