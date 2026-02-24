from django.core.exceptions import ValidationError
from django.utils import timezone
from apps_.promotions.models import PromotionToProduct, PromotionToSeller
from config.core import INTEREST_RATES, AVAILABLE_PERIODS
from decimal import Decimal




class PricingService:
    CURRENCY = 'UZB'
    
    
    @staticmethod
    def get_price(product):
        if not hasattr(product, 'price') or product.price is None:
            return ValidationError('bu maxsulotda narx mavjud emas')
        
        price = product.price
        
        base_price = price.price
        discounted_price = price.chegirma if price.chegirma is not None else 0
        discount_percent = (discounted_price / base_price) * 100
        final_price = base_price - discounted_price
        
        return {
            'base_price':base_price,
            'discounted_price':discounted_price,
            'final_price':final_price,
            'discount_percent':int(discount_percent),
            'currency':PricingService.CURRENCY
        }
        
    
   
    def calculate_monthly_payment(product_price, month):
        if not month in INTEREST_RATES:
            return ValidationError('bu oy foiz oylarida yuq')
        
        interest = INTEREST_RATES[month]
        total_with_interest = product_price + (product_price * Decimal(interest) / 100)
        monthly_payment = total_with_interest / month
        
        return int(monthly_payment)
        
    def get_installments(self, product):
        if not hasattr(product, 'price') or product.price is None:
            return ValidationError('bu maxsulotda narx mavjud emas')
        
        total_price = product.price.price
        
        if total_price is None or total_price <=0:
            return ValidationError('maxsulot narxi valid emas')
        
        installments = []
        for month in AVAILABLE_PERIODS:
            try:
                monthly_payment =  self.calculate_monthly_payment(Decimal(total_price), month)
                installments.append({
                    'months':month,
                    'monthly_price':monthly_payment,
                    'interest':INTEREST_RATES[month]
                })
            except Exception:
                continue
    
        return installments
        
        
class PromotionService:
    
    @staticmethod
    def get_active_promotions_for_product(product):
        now = timezone.now()
        return product.promotions.filter(start_date__lte=now, end_date__gte=now)
    
    @staticmethod
    def get_active_promotions_for_seller(seller):
        now = timezone.now()
        return seller.promotions.filter(start_date__lte=now, end_date__gte=now)
    
    @staticmethod
    def get_promotion_by_code(code):
        now = timezone.now()
        product_promotion = PromotionToProduct.objects.filter(code=code, start_date__lte=now, end_date__gte=now).first()
        if product_promotion is not None:
            return {
                'id': product_promotion.id,
                'type':'product',
                'interest': product_promotion.interest,
            
            }
        if not product_promotion:
            seller_promotion = PromotionToSeller.objects.filter(code=code, start_date__lte=now, end_date__gte=now).first()
            if seller_promotion is not None:
                return {
                    'id': seller_promotion.id,
                    'type':'seller',
                    'interest': seller_promotion.interest,
                    
                }
        return None
    
    @staticmethod
    def check_user_promotion(user, promotion_id, promotion_type):
        if promotion_type == 'product':
            return user.used_promotions.filter(promotion_id=promotion_id, promotion_type='product').exists()
        elif promotion_type == 'seller':
            return user.used_promotions.filter(promotion_id=promotion_id, promotion_type='seller').exists()
        return False