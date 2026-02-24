from django.db import transaction
from apps_.promotions.services import PricingService
from apps_.orders.services import AnaliticOrdersService
from apps_.reviews.services import ReviewService
from apps_.categories.services import CategoryService
from .models import Product
from .models import Product

from django.utils import timezone
from apps_.orders.models import Order, OrderItem


class ProductAnalyticsService:
    @staticmethod
    def get_daily_product_sales(product_id):
        today = timezone.now().date()
        return OrderItem.objects.filter(product_id=product_id, order__order_date__date=today).count()

    @staticmethod
    def get_total_products():
        return Product.objects.count()

    @staticmethod
    def get_out_of_stock_count():
        return Product.objects.filter(stock__lte=0).count() if hasattr(Product, 'stock') else 0

    @staticmethod
    def get_product_count_by_category():
        from django.db.models import Count
        return Product.objects.values('category__name').annotate(count=Count('id')).order_by('-count')

    @staticmethod
    def get_weekly_product_sales(product_id):
        week_ago = timezone.now() - timezone.timedelta(days=7)
        return OrderItem.objects.filter(product_id=product_id, order__order_date__gte=week_ago).count()

    @staticmethod
    def get_total_product_sales(product_id):
        return OrderItem.objects.filter(product_id=product_id).count()

    @staticmethod
    def get_canceled_product_orders(product_id):
        return Order.objects.filter(items__product_id=product_id, status=Order.OrderStatus.CANCELED).distinct().count()


@transaction.atomic
def get_or_create_product(seller):
    product, _ = Product.objects.get_or_create(seller=seller)
    return product



def calculate_price_discount(price, chegirma_price):
    if price > chegirma_price:
        final_price = price - chegirma_price
        if chegirma_price is None or int(chegirma_price) == 0:
            return final_price, 0
        percent = (chegirma_price / price) * 100
    return final_price, int(percent)
        

class ProductDetailService:

    @staticmethod
    def get_details(product, user, request):
        return {
            'id': product.id,
            'detail': product.detail,
            'certificates': product.certificates if product.certificates else 'bu maxsulotda sertifikat yuq',
            'instructions': product.instructions if product.instructions else 'bu maxsulotda instructions yuq',
            'bredcrumbs': CategoryService.get_category_breadcrumbs(product.category),
            'offer': PricingService.get_price(product=product),
            'installments': PricingService.get_installments(PricingService, product),
            'media': product.get_media(request),
            'stock': product.get_stock(), 
            'social_proof': AnaliticOrdersService.get_weekly_purchases(product.id),
            'reviews': ReviewService.get_product_reviews(product),
            'delivery' : 'Manzilga qarab 4 soat yoki 3 ish kun ichida yetkazib beriladi'
            
        }

    
