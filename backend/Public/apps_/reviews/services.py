from django.core.exceptions import ValidationError
from django.db import models
from .models import Review, ReviewImage
from config.settings import BASE_DOMEN

from django.utils import timezone


class ReviewAnalyticsService:
    @staticmethod
    def get_daily_reviews():
        today = timezone.now().date()
        return Review.objects.filter(created_at__date=today).count()

    @staticmethod
    def get_weekly_reviews():
        week_ago = timezone.now() - timezone.timedelta(days=7)
        return Review.objects.filter(created_at__gte=week_ago).count()

    @staticmethod
    def get_total_reviews():
        return Review.objects.count()

    @staticmethod
    def get_average_rating():
        return Review.objects.aggregate(avg=models.Avg('rating'))['avg'] or 0

class ReviewService:
    
    
    @staticmethod
    def get_product_reviews(product):
        if not product:
            raise ValidationError('product kelmadi')
        reviews = Review.objects.filter(product=product)
        
        review_list = []
        for review in reviews[:5]:
            review_list.append({
                'id': review.id,
                'user': review.user.email,
                'rating': review.rating,
                'afzallik': review.afzallik,
                'kamchilik': review.kamchilik,
                'izoh': review.izoh,
                'created_at': review.created_at,
                'images': [f"{BASE_DOMEN}{image.image.url}" for image in review.images.all()]
            })
        return review_list
    
    @staticmethod
    def get_product_reviews_and_rating_count(product):
        if not product:
            raise ValidationError('product kelmadi')
        rating  = Review.objects.filter(product=product).aggregate(average_rating=models.Avg('rating'))['average_rating'] or 0
        count = Review.objects.filter(product=product).count()
        return {
            'count': count,
            'rating': rating
        }
    