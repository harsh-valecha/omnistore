from django.contrib import admin
from .models import Discount, DiscountRule


class DiscountRuleInline(admin.TabularInline):
    model = DiscountRule
    extra = 0


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_type', 'value', 'is_active', 'is_valid', 'active_from', 'active_until']
    list_filter = ['discount_type', 'is_active']
    search_fields = ['code']
    inlines = [DiscountRuleInline]


@admin.register(DiscountRule)
class DiscountRuleAdmin(admin.ModelAdmin):
    list_display = ['discount', 'min_order_value', 'limit_per_user', 'category']
    list_filter = ['discount']
