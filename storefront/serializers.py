from rest_framework.serializers import ModelSerializer
from .models import Product,Category

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','description','image','brand','category','created_at','is_active','price']
        extra_kwargs={
            'created_at':{'read_only':True},
            'updated_at':{'read_only':True},
        }

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','created_at']
        extra_kwargs={
            'created_at':{'read_only':True}
        }