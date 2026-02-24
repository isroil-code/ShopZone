from django_filters import rest_framework as filters
from .models import Product
from apps_.categories.models import Category
from apps_.categories.services import CategoryService


class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price__price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price__price", lookup_expr="lte")

    category_id = filters.NumberFilter(method="filter_category_id")
    name = filters.CharFilter(field_name="detail__name", lookup_expr="icontains")
    status = filters.ChoiceFilter(choices=Product.Status.choices)
    
    created_after = filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")
    
    def filter_category_id(self, qs, name, value):
        category = Category.objects.get(id=value)
        category_ids = CategoryService.get_category_and_children_ids(category)
        return qs.filter(category_id__in=category_ids)

    class Meta:
        model = Product
        fields = ['min_price', 'max_price', 'category_id', 'name', 'status', 'created_after', 'created_before']
    