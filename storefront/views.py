from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .permissions import IsAdminOrReadOnly
from .models import Cart, CartItem, Category, Order, Product, Reveiw
from .serializers import CartItemSerializer, CartSerializer, OrderSerializer, ProductSerializer,CategorySerializer, ReveiwSerializer
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
    

class CartItemViewset(ModelViewSet):
    serializer_class=CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart= get_object_or_404(Cart, user = self.request.user)

        if cart.id and cart.id == int(self.kwargs['cart_pk']):
            return CartItem.objects.filter(cart=self.kwargs['cart_pk'])
        
        raise PermissionDenied("You are not allowed to view this cart.")
    
    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk']}

class OrderViewset(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ['get','post']