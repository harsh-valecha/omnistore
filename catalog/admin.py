from django.contrib import admin
from .models import Category, Product, ProductVariant, StockItem


class StockItemInline(admin.TabularInline):
    model = StockItem
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'base_price', 'status', 'created_at']
    list_filter = ['status', 'category']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['sku', 'product', 'size', 'color', 'price', 'is_active']
    list_filter = ['is_active', 'product']
    search_fields = ['sku', 'product__name']


@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    list_display = ['variant', 'quantity', 'location', 'is_low_stock']
    list_filter = ['location']
    search_fields = ['variant__sku']
