from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from .permissions import IsAdminOrReadOnly
from .models import Cart, CartItem, Category, Order, Product, Reveiw
from .serializers import CartItemSerializer, CartSerializer, CreateOrderSerializer,  OrderSerializer, ProductSerializer,CategorySerializer, ReveiwSerializer, UpdateOrder
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
        if self.request.user.is_staff:
            return Cart.objects.all()
        return Cart.objects.filter(user=self.request.user)
    

class CartItemViewset(ModelViewSet):
    serializer_class=CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart= get_object_or_404(Cart, user = self.request.user)

        if self.request.user.is_staff:
            return CartItem.objects.filter(cart=self.kwargs['cart_pk'])

        elif cart.id and cart.id == int(self.kwargs['cart_pk']):
            return CartItem.objects.filter(cart=self.kwargs['cart_pk'])
        
        raise PermissionDenied("You are not allowed to view this cart.")
    
    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk']}

class OrderViewset(ModelViewSet):
    http_method_names = ['patch','delete','get','options','head']
    
    def get_permissions(self):
        if self.request.method in ['PATCH','DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data, context = {'request':self.request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrder
        return OrderSerializer