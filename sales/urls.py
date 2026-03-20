from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/<int:pk>/update-status/', views.update_order_status, name='update_order_status'),
]
