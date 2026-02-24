from .models import Cart
from apps_.payments.services import FinalPricing
from decimal import Decimal

pricing = FinalPricing()


def create_cart(user): 
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart
    
def calculate_cart_total(cart):
    total = Decimal(0)
    base = Decimal(0)
    
    for item in cart.items.filter(is_selected=True):
        try:
            product_id = item.product.pk
            quantity = item.quantity
            discounted_price, base_price = pricing.get_price(product_id, quantity)
            total += Decimal(discounted_price)
            base += Decimal(base_price)
        except Exception:
                pass
    return {
        "total": total,
        "base": base,
        'tejov': base - total
    }
        
