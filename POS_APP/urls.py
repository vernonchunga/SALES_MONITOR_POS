from django.urls import path
from . import views 

app_name = 'POS_APP'

urlpatterns = [
    path('', views.product_list, name='product-list'),
    path('product_add/', views.Product_add, name='product-add'),
    path('product_update', views.product_list, name='product-list')
]