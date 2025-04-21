from rest_framework import serializers
from .models import Cart, CartItem, Product,Category, Reveiw

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
    product = serializers.Serializer
    class Meta:
        model = CartItem
        fields = ['id','quantity','cart','product']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    class Meta:
        model = Cart
        fields = ['id','user','created_at','items']
        etxtra_kwargs={
            'user':{'read_only':True},
            'created_at':{'read_only':True},
            'id':{'read_only':True}
        }