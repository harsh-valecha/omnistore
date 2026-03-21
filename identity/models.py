from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        MANAGER = 'manager', 'Manager'
        STAFF = 'staff', 'Staff'

    role = models.CharField(max_length=20, choices=Role, default=Role.STAFF)

    class Meta:
        permissions = [
            ('view_all_orders', 'Can view all orders across all statuses'),
            ('manage_inventory', 'Can manage product inventory'),
            ('manage_discounts', 'Can manage discounts and promotions'),
        ]

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_manager(self):
        return self.role == self.Role.MANAGER

    @property
    def is_staff_member(self):
        return self.role == self.Role.STAFF
