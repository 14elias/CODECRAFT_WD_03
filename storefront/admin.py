from django.contrib import admin
from .models import Cart, Order, OrderItem, Product,Category,Reveiw,CartItem
# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Reveiw)
admin.site.register(CartItem)
admin.site.register(OrderItem)
admin.site.register(Order)

class CartAdmin(admin.ModelAdmin):
    list_display = ['id','created_at','user__first_name']

admin.site.register(Cart,CartAdmin)