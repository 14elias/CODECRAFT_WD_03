from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import Cart, CartItem, Order, OrderItem, Product,Category, Reveiw

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','description','image','brand','category','created_at','is_active','price']
        extra_kwargs={
            'created_at':{'read_only':True},
            'updated_at':{'read_only':True},
        }

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','created_at']
        extra_kwargs={
            'created_at':{'read_only':True}
        }

class ReveiwSerializer(serializers.ModelSerializer):
    user=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Reveiw
        fields = ['id','name','product','created_at','description','user']
        extra_kwargs={
            'product':{'read_only':True}
        }
    
    def get_user(self,obj):
        return obj.user.first_name
    
    def create(self, validated_data):
        user = self.context['request'].user
        product_id = self.context['product_id']
        review = Reveiw.objects.create(user=user,product_id=product_id,**validated_data)
        return review

class CartItemSerializer(serializers.ModelSerializer):
    product_name=serializers.SerializerMethodField()
    product_price = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ['id','quantity','product','product_name','product_price','total_price']
    
    def get_product_name(self,obj):
        return obj.product.name
    
    def get_product_price(self,obj):
        return obj.product.price
    
    def get_total_price(self,obj):
        #calling object method implemented in models file
        return obj.get_total_price()
    
    def create(self, validated_data):
        cart_id = self.context.get('cart_id')
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')

        cart_item = CartItem.objects.filter(cart_id=cart_id, product=product).first()

        if cart_item :
            cart_item.quantity += quantity
            cart_item.save()
            return cart_item
        
        return CartItem.objects.create(cart_id = cart_id,**validated_data)
    
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id','user','created_at','items','total_price']
        extra_kwargs={
            'user':{'read_only':True},
            'created_at':{'read_only':True},
            'id':{'read_only':True}
        }

    def get_total_price(self,obj):
        return sum([item.product.price * item.quantity for item in obj.items.all() ])
    
class OrderItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    product = ProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id','product','quantity','price','total_price']

    def get_total_price(self,obj):
        return obj.get_total_price()
    
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many = True)
    class Meta:
        model = Order
        fields = ['id','user','created_at','status','items']

    
class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField()

    def validate_cart_id(self,cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('no cart found with the given id')
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError('The cart is empty')
        return cart_id
    
    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            user = self.context['request'].user

            if cart_id != user.cart.id:
                raise PermissionDenied("the cart is not your's")

            cart_items = CartItem.objects.filter(cart_id=cart_id)
            
            order = Order.objects.create(user=user)

            order_item = [OrderItem(
                order = order,
                product = items.product,
                quantity = items.quantity,
                price = items.product.price
            ) for items in cart_items]

            OrderItem.objects.bulk_create(order_item)
            cart_items.delete()

            return order