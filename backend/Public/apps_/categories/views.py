from django.shortcuts import render
from rest_framework.generics import ListAPIView,RetrieveAPIView
from .serializers import CategorySerializer, CategoryDetailSerializer
from .models import Category
from rest_framework.viewsets import ModelViewSet
from config.permissions import IsAdmin

class CategoryView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(parent__isnull=True)
    
class CategoryDetailView(ListAPIView):
    serializer_class = CategoryDetailSerializer
    queryset = Category.objects.all()
  
    
    def get_queryset(self):
        parent = self.request.query_params.get('parent', None)     
        queryset = Category.objects.filter(is_active=True)
    
        if parent is None:
            return queryset.filter(parent__isnull=True)
        return queryset.filter(parent_id=parent)
    
    

# Admin views

class CategoryAdminView(ModelViewSet):
    permission_classes = [IsAdmin]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()



    
    
    
