from django.contrib import admin
from .models import Product,Category,Reveiw,CartItem
# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Reveiw)
admin.site.register(CartItem)