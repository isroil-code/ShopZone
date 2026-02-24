from random import random
from django.core.exceptions import ValidationError
from apps_.products.models import Product
from .models import Order, OrderItem
from apps_.payments.services import FinalPricing
from django.utils import timezone   
from django.shortcuts import get_object_or_404



        

class OrderService:
    
    @staticmethod
    def order_create(cart, request):
        if not cart and not cart.items.exists():
            raise ValidationError('cart bo\'sh')
        
        order = Order.objects.create(
            user=request.user, 
            final_quantity=0,
            base_price=0,
            discounted_price=0
        )
        
        final_quantity = 0
        base_price = 0
        discounted_price = 0
     
        
        for item in cart.items.filter(is_selected=True):
            product_id = item.product.pk
            quantity = item.quantity
            pricing = FinalPricing()
            item_discounted_price, item_base_price = pricing.get_price(product_id, quantity)

            OrderItem.objects.create(order=order, product=item.product, quantity=quantity, full_price=item_base_price)

    
            product_stock = item.product.stock
            if product_stock.quantity < quantity:
                raise ValidationError(f"Stockda yetarli mahsulot yo'q: {item.product.detail.name}")
            product_stock.quantity -= quantity
            product_stock.save(update_fields=['quantity'])

            final_quantity += quantity
            discounted_price += item_discounted_price
            base_price += item_base_price

        order.final_quantity = final_quantity
        order.base_price = base_price
        order.discounted_price = discounted_price
        order.save(update_fields=['final_quantity', 'base_price', 'discounted_price'])

        cart.items.all().delete()
        return order
        

    @staticmethod
    def order_cancel(order):
        if order.status == Order.OrderStatus.CANCELED:
            raise ValidationError('bu order alaqachon bekor qilingan')
        if order.status == Order.OrderStatus.DELIVERED and order.payments.status == Order.OrderStatus.IS_PAID:
            raise ValidationError('bu order ni bekor qilolmaysiz ')
        
        order.status = Order.OrderStatus.CANCELED
        order.save(update_fields=['status'])

        
class AnaliticOrdersService:
    
    @staticmethod
    def get_total_orders_numder():
        
        product = Product.objects.filter(seller__id=2)
        count = 0
        for p in product.all():
            count += p.orders.count()
            
        return count

    @staticmethod
    def get_orders_per_day():
        today = timezone.now().date()
        return Order.objects.filter(order_date__date=today).count()

    @staticmethod
    def get_pending_count():
        return Order.objects.filter(status=Order.OrderStatus.PENDING).count()

    @staticmethod
    def get_cancelled_count():
        return Order.objects.filter(status=Order.OrderStatus.CANCELED).count()

    @staticmethod
    def get_completed_count():
        return Order.objects.filter(status=Order.OrderStatus.DELIVERED).count()

    @staticmethod
    def get_average_processing_time():
        from django.db.models import Avg, F, ExpressionWrapper, DurationField
        qs = Order.objects.filter(delivered_date__isnull=False, order_date__isnull=False)
        if not qs.exists():
            return None
        avg_time = qs.annotate(
            processing_time=ExpressionWrapper(F('delivered_date') - F('order_date'), output_field=DurationField())
        ).aggregate(avg=Avg('processing_time'))['avg']
        return avg_time

    @staticmethod
    def get_daily_orders_count():
        today = timezone.now().date()
        return Order.objects.filter(order_date__date=today).count()

    @staticmethod
    def get_weekly_orders_count():
        week_ago = timezone.now() - timezone.timedelta(days=7)
        return Order.objects.filter(order_date__gte=week_ago).count()

    @staticmethod
    def get_canceled_orders_count():
        return Order.objects.filter(status=Order.OrderStatus.CANCELED).count()


    @staticmethod
    def get_weekly_purchases(product_id):
        product = get_object_or_404(Product, pk=product_id)
        if product.orders.exists():
            purchases = product.orders.filter(order__order_date__gte=timezone.now() - timezone.timedelta(days=7)).count()
            return {'purchases': purchases}
        return {'purchases': 0}
    
    

