from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly
from .models import Cart, Category, Product, Reveiw
from .serializers import CartSerializer, ProductSerializer,CategorySerializer, ReveiwSerializer
from.pagination import DefaultPagination

class ProductViewset(ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class=DefaultPagination

    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.request.query_params.get('category_id')
        if category_id is not None:
            return  queryset.filter(category_id=category_id)
        return queryset

class CategoryViewset(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class ReveiwViewset(ModelViewSet):
    serializer_class = ReveiwSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reveiw.objects.filter(product_id=self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk'],'request':self.request}
class CartViewset(ModelViewSet):
    serializer_class = CartSerializer
    permission_classes=[IsAuthenticated]
    http_method_names=['get']

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)