from django.contrib import admin
from django.contrib.admin.filters import RelatedFieldListFilter
from .models import Category


class ParentCategoryFilter(RelatedFieldListFilter):
    def field_choices(self, field, request, model_admin):
        return field.get_choices(include_blank=False, limit_choices_to={'parent__isnull': True})


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'order', 'get_children_count']
    list_filter = [('parent', ParentCategoryFilter)]
    search_fields = ['name', 'slug']
    ordering = ['order', 'name']
    # prepopulated_fields = {'slug': ('name',)}
    
    def get_children_count(self, obj):
        return obj.children.count()
    get_children_count.short_description = 'Subcategories'
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('children')
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'parent':
            # Exclude the current object and its descendants to prevent circular references
            if hasattr(request, '_obj') and request._obj:
                descendants = self.get_descendants(request._obj)
                kwargs['queryset'] = Category.objects.exclude(pk__in=[request._obj.pk] + list(descendants.values_list('pk', flat=True)))
            else:
                kwargs['queryset'] = Category.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_descendants(self, category):
        descendants = set()
        children = category.children.all()
        for child in children:
            descendants.add(child)
            descendants.update(self.get_descendants(child))
        return descendants