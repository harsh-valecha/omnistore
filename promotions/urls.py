from django.urls import path
from . import views

app_name = 'promotions'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('discounts/', views.discount_list, name='discount_list'),
    path('discounts/<int:pk>/', views.discount_detail, name='discount_detail'),
]
