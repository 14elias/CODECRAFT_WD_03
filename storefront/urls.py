from django.urls import path
from.views import ProductViewset

urlpatterns = [
    path('product/',ProductViewset.as_view({'get': 'list'}))
]