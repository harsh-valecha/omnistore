from django.db import models
from django.core.exceptions import ValidationError
from catalog.models import Category, Product


class Discount(models.Model):
    class DiscountType(models.TextChoices):
        PERCENTAGE = 'percentage', 'Percentage'
        FLAT = 'flat', 'Flat Amount'

    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=20, choices=DiscountType)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    active_from = models.DateTimeField()
    active_until = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    categories = models.ManyToManyField(
        Category,
        blank=True,
        related_name='discounts'
    )
    products = models.ManyToManyField(
        Product,
        blank=True,
        related_name='discounts'
    )
    usage_limit = models.IntegerField(
        null=True,
        blank=True,
        help_text='Maximum number of times this discount can be used'
    )
    usage_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

    def clean(self):
        if self.discount_type == 'percentage' and self.value > 100:
            raise ValidationError({'value': 'Percentage discount cannot exceed 100%'})

    @property
    def is_valid(self):
        from django.utils import timezone
        now = timezone.now()
        return (
            self.is_active
            and self.active_from <= now <= self.active_until
            and (self.usage_limit is None or self.usage_count < self.usage_limit)
        )


class DiscountRule(models.Model):
    discount = models.ForeignKey(
        Discount,
        on_delete=models.CASCADE,
        related_name='rules'
    )
    min_order_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    limit_per_user = models.IntegerField(
        null=True,
        blank=True,
        help_text='Maximum uses per user'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='discount_rules'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rule for {self.discount.code}"
