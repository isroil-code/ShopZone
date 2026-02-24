from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'order', 'children']
        
    def get_children(self, obj):
        children_qs = obj.children.filter(parent_id=obj.id, is_active=True).order_by('order')
        return CategorySerializer(children_qs, many=True, context=self.context).data

    
    
class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'order']