from rest_framework.serializers import ModelSerializer,SerializerMethodField
from .models import Product,Category, Reveiw

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

class ReveiwSerializer(ModelSerializer):
    user=SerializerMethodField(read_only=True)
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