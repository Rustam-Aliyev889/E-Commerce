from django.urls import path
from .views import product_list, product_detail, create_product


urlpatterns = [
    path('list/', product_list, name='product_list'),  # Adjust the URL pattern as needed
    path('<int:pk>/', product_detail, name='product_detail'),
    path('create/', create_product, name='create_product'),
]