from unicodedata import category
from django.core.exceptions import ValidationError
from .models import Category


class CategoryService:
    
    @staticmethod
    def get_category_breadcrumbs(category):
        if not category:
            return None
        
        breadcrumbs = []
        current_category = category
        
        while current_category is not None:
            breadcrumbs.append({
                'id': current_category.id,
                'name': current_category.name,
                'slug': current_category.slug
            })
            current_category = current_category.parent
            
        return breadcrumbs[::-1]
    
    @staticmethod
    def get_children_categories(category):
        if not category:
            raise ValidationError('category kelmadi')
        children = []

        def _collect_children(cat):
            for child in cat.children.filter(is_active=True):
                children.append(child)
                _collect_children(child)

        _collect_children(category)
        return children

    @staticmethod
    def get_category_and_children_ids(category):
        if not category:
            raise ValidationError('category kelmadi')

        ids = [category.id]
        for child in CategoryService.get_children_categories(category):
            ids.append(child.id)
        return ids