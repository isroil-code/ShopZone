from rest_framework import serializers
from .models import Review, ReviewImage


class ReviewCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )
    
    class Meta:
        model = Review
        fields = ['id', 'rating', 'afzallik', 'kamchilik', 'izoh', 'images']
        
    def create(self, validated_data):
        images = validated_data.pop('images', [])
        review = Review.objects.create(**validated_data)
        
        if images:  
            for image in images:
                ReviewImage.objects.create(review=review, image=image)
        
        return review
    
class ReviewListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    user_email = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = ['id', 'user_email', 'rating', 'afzallik', 'kamchilik', 'izoh', 'images', 'created_at']
        
    def get_images(self, obj):
        return [image.image.url for image in obj.images.all()]
    
    def get_user_email(self, obj):
        return obj.user.email