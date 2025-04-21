from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from django.urls import path
from.views import CartViewset, ProductViewset,CategoryViewset, ReveiwViewset

#main router
router = DefaultRouter()
router.register(r'product', ProductViewset, basename='product')
router.register(r'category', CategoryViewset, basename='category')
router.register(r'cart',CartViewset, basename='cart')

#default router
product_router=NestedDefaultRouter(router, r'product', lookup='product')
product_router.register(r'review',ReveiwViewset,basename='product-review')

urlpatterns = router.urls + product_router.urls