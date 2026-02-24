from django.shortcuts import render
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework import permissions as p
from .models import Cart, CartItem, Wishlist, WishlistItems
from apps_.products.models import Product
from rest_framework.response import Response
from .serialzers import CartSerialzier, WishListSerializer
from apps_.orders.services import AnaliticOrdersService

class AddToCart(GenericAPIView):
    permission_classes = [p.IsAuthenticated]
    
    def post(self, request, pk, *args, **kwargs):
        user = self.request.user
        
        cart, _ = Cart.objects.get_or_create(user=user)
        product = Product.objects.get(pk=pk)
        if product.stock.quantity <= 0:
            return Response({'detail':'bu maxsulot sotuvda yuq yoq'}, status=400)
        
        
        check_card = CartItem.objects.filter(cart=cart, product=product).exists()
        if check_card:
            return Response({'detail':'bu maxsulot cart da bor'}, status=401)
        if cart and product:
            CartItem.objects.create(
                cart=cart,
                product=product
            )
        
            return Response({'detail':'Product cart ga qushildi', 'product_name':product.detail.name if hasattr(product, 'detail') else 'unknown'}, status=200)
        return Response({'detail':'Product cart ga qushilmadi'}, status=400)
        
        
class DeleteFromCart(GenericAPIView):
    permission_classes = [p.IsAuthenticated]
    
    def delete(self, request, pk, *args, **kwargs):
        user = self.request.user
        
        cart, _ = Cart.objects.get_or_create(user=user)
        product = Product.objects.get(pk=pk)
        
        check_card = CartItem.objects.filter(cart=cart, product=product).exists()
        if not check_card:
            return Response({'detail':'bu maxsulot allaqachin uchirligan'}, status=400)
            
        CartItem.objects.filter(cart=cart, product=product).delete()
        return Response({'detail':'product has been deleted'}, status=200)

class IncreaseQuantityView(GenericAPIView):
    permission_classes = [p.IsAuthenticated]
    
    def post(self, request, pk, *args, **kwargs):
        user = self.request.user
        
        cart, _ = Cart.objects.get_or_create(user=user)
        product = Product.objects.get(pk=pk)
        if cart and product:
            cart_item = CartItem.objects.filter(cart=cart, product=product).first()
            if cart_item:
                    if cart_item.quantity >= product.stock.quantity:
                        return Response({'detail': 'Stockda yetarli mahsulot yo\'q', 'max_stock': product.stock.quantity}, status=400)
                    cart_item.quantity += 1
                    cart_item.save(update_fields=['quantity'])
                    return Response({'detail':'quantity increased', 'quantity':cart_item.quantity}, status=200)
        return Response({'detail':'nimadir xato ketti'},status=400)
    
class DecreaseQuantityView(GenericAPIView):
    permission_classes = [p.IsAuthenticated]
    
    def post(self, request, pk, *args, **kwargs):
        user = self.request.user
        
        cart, _ = Cart.objects.get_or_create(user=user)
        product = Product.objects.get(pk=pk)
        if cart and product:
            cart_item = CartItem.objects.filter(cart=cart, product=product).first()
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save(update_fields=['quantity'])
                return Response({'detail':'quantity decreased', 'quantity':cart_item.quantity}, status=200)
            return Response({'detail':'quantity remined', 'quantity':cart_item.quantity}, status=200)
        return Response({'detail':'nimadir xato ketti'},status=400)
    
    
class SelectCartItemView(GenericAPIView):
    permission_classes = [p.IsAuthenticated]
    
    def post(self, request, pk, *args, **kwargs):
        user = self.request.user
        
        cart, _ = Cart.objects.get_or_create(user=user)
        product = Product.objects.get(pk=pk)
        if cart and product:
            cart_item = CartItem.objects.filter(cart=cart, product=product).first()
            if cart_item.is_selected:
                cart_item.is_selected = not cart_item.is_selected
                cart_item.save(update_fields=['is_selected'])
                return Response({'detail':'maxsulot tanlanmadi', 'is_selected':cart_item.is_selected}, status=200)
            else:
                cart_item.is_selected = not cart_item.is_selected
                cart_item.save(update_fields=['is_selected'])
                return Response({'detail':'maxsulot tanlandi', 'is_selected':cart_item.is_selected}, status=200)
        return Response({'detail':'nimadir xato ketti'},status=400)

class CartView(ListAPIView):
    permission_classes = [p.IsAuthenticated]
    serializer_class = CartSerialzier
    queryset = Cart.objects.all()
    
    def get_queryset(self):
        user = self.request.user
        if not Cart.objects.filter(user=user).exists():
            Cart.objects.create(user=user)
        return Cart.objects.filter(user=user)
    
        
class AddToWishlist(GenericAPIView):
    permission_classes = [p.IsAuthenticated]
    
    
    def post(self, request, pk, *args, **kwargs):
        wishlist, _ = Wishlist.objects.get_or_create(user=self.request.user)
        product = Product.objects.get(pk=pk)
        
        check_wishlist = WishlistItems.objects.filter(wishlist=wishlist, product=product).exists()
        
        if check_wishlist:
            return Response({'detail':'bu maxsulot mavjud'})
        
        if wishlist is not None and product:
            item = WishlistItems.objects.create(
                wishlist=wishlist,
                product=product
            )
            return Response({'detail':'wishlistga product qushildi', 'product_id':product.pk}, status=200)
        return Response({'detail':'wishlistga product qushilmadi'}, status=400)
    
class DeleteFromWishlist(GenericAPIView):
    permission_classes = [p.IsAuthenticated]
    
    def delete(self, request, pk, *args, **kwargs):
        wishlist, _ = Wishlist.objects.get_or_create(user=self.request.user)
        product = Product.objects.get(pk=pk)
        
        if wishlist is not None and product:
            item = WishlistItems.objects.filter(wishlist=wishlist, product=product).delete()
            return Response({'detail':'wishlistdan product uchirildi', 'product_id':product.pk}, status=200)
        return Response({'detail':'wishlistdan product uchirilmadi'}, status=400)


        
class WishlistView(ListAPIView):
    permission_classes = [p.IsAuthenticated]
    serializer_class = WishListSerializer
    
    def get_queryset(self):
        user = self.request.user
        wishlist = Wishlist.objects.filter(user=user).exists()
        if not wishlist:
            Wishlist.objects.create(user=user)
        return Wishlist.objects.filter(user=user)
        
            
