from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('categories/', views.category_list, name='category_list'),
]
