from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from django.urls import path
from.views import CartItemViewset, CartViewset, ProductViewset,CategoryViewset, ReveiwViewset

#main router
router = DefaultRouter()
router.register(r'product', ProductViewset, basename='product')
router.register(r'category', CategoryViewset, basename='category')
router.register(r'cart', CartViewset, basename='cart')

#default router
product_router=NestedDefaultRouter(router, r'product', lookup='product')
product_router.register(r'review',ReveiwViewset,basename='product-review')

cart_router = NestedDefaultRouter(router, r'cart', lookup='cart')
cart_router.register(r'items', CartItemViewset, basename ='cart_items')

urlpatterns = router.urls + product_router.urls + cart_router.urls