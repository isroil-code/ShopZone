from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['name', 'slug', 'parent', 'order', 'children']
        
    def get_children(self, obj):
        children_qs = obj.children.all().order_by('order')
        return CategorySerializer(children_qs, many=True, context=self.context).data

    def create(self, validated_data):
        parent = validated_data.get('parent', None)
        if validated_data.get('order') in (None, 0):
            from django.db.models import Max
            if parent:
                sibling_max = parent.children.aggregate(max_order=Max('order'))['max_order']
                validated_data['order'] = (sibling_max or 0) + 1
            else:
                root_max = Category.objects.filter(parent__isnull=True).aggregate(max_order=Max('order'))['max_order']
                validated_data['order'] = (root_max or 0) + 1
        return super().create(validated_data)
    
    
class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'parent', 'order']