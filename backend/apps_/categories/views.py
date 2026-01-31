from django.shortcuts import render
from rest_framework.generics import ListAPIView,RetrieveAPIView
from .serializers import CategorySerializer
from .models import Category
from rest_framework.viewsets import ModelViewSet

class CategoryView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(parent__isnull=True)
    
class CategoryDetailView(RetrieveAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'slug'
    
    def get_queryset(self):
        return Category.objects.filter(slug=self.kwargs['slug'])
    
    
    
# Admin views

class CategoryAdminView(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(parent__isnull=True)



    
    
    
