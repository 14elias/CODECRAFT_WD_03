from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from django.urls import path
from.views import ProductViewset,CategoryViewset

router = DefaultRouter()
router.register(r'product', ProductViewset, basename='product')
router.register(r'category', CategoryViewset, basename='category')

urlpatterns = router.urls