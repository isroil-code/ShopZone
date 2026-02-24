from django.db import transaction
from .models import Seller, SellerBalance, Shartnoma

from django.utils import timezone
from apps_.orders.models import Order, OrderItem
from apps_.products.models import Product



@transaction.atomic
def create_shartnoma(seller):
    shartnoma = Shartnoma.objects.create(seller=seller)
    return shartnoma    

@transaction.atomic
def create_seller_balnce(seller):
    balance = SellerBalance.objects.create(seller=seller)
    return balance


class SellerAnalyticsService:
    @staticmethod
    def get_daily_seller_sales(seller_id):
        today = timezone.now().date()
        return OrderItem.objects.filter(product__seller_id=seller_id, order__order_date__date=today).count()

    @staticmethod
    def get_total_sellers():
        return Seller.objects.count()

    @staticmethod
    def get_active_sellers():
        month_ago = timezone.now() - timezone.timedelta(days=30)
      
        return Seller.objects.filter(products__orders__order__order_date__gte=month_ago).distinct().count()

    @staticmethod
    def get_pending_verification_sellers():
        return Seller.objects.filter(status=Seller.Status.PENDING).count()

    @staticmethod
    def get_weekly_seller_sales(seller_id):
        week_ago = timezone.now() - timezone.timedelta(days=7)
        return OrderItem.objects.filter(product__seller_id=seller_id, order__order_date__gte=week_ago).count()

    @staticmethod
    def get_total_seller_sales(seller_id):
        return OrderItem.objects.filter(product__seller_id=seller_id).count()

    @staticmethod
    def get_canceled_seller_orders(seller_id):
        return Order.objects.filter(items__product__seller_id=seller_id, status=Order.OrderStatus.CANCELED).distinct().count()


