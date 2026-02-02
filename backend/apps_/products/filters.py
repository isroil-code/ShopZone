from django_filters import rest_framework as filters
from .models import Product

class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price__price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price__price", lookup_expr="lte")

    category_id = filters.NumberFilter(field_name="category_id")
    name = filters.CharFilter(field_name="detail__name", lookup_expr="icontains")
    status = filters.ChoiceFilter(choices=Product.Status.choices)
    
    created_after = filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Product
        fields = ['min_price', 'max_price', 'category_id', 'name', 'status', 'created_after', 'created_before']
    