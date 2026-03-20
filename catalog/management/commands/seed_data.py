from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random

from identity.models import User
from catalog.models import Category, Product, ProductVariant, StockItem
from promotions.models import Discount, DiscountRule
from sales.models import Order, OrderItem, OrderStatusHistory


class Command(BaseCommand):
    help = 'Seeds the database with sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # Create users
        users = self.create_users()
        self.stdout.write(f'Created {len(users)} users')

        # Create categories
        categories = self.create_categories()
        self.stdout.write(f'Created {len(categories)} categories')

        # Create products
        products = self.create_products(categories)
        self.stdout.write(f'Created {len(products)} products')

        # Create variants
        variants = self.create_variants(products)
        self.stdout.write(f'Created {len(variants)} product variants')

        # Create stock items
        self.create_stock_items(variants)
        self.stdout.write(f'Created stock items for {len(variants)} variants')

        # Create discounts
        discounts = self.create_discounts(categories, products)
        self.stdout.write(f'Created {len(discounts)} discounts')

        # Create orders
        orders = self.create_orders(users, variants)
        self.stdout.write(f'Created {len(orders)} orders')

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))

    def create_users(self):
        users_data = [
            {'username': 'admin', 'email': 'admin@omnistore.com', 'role': 'admin', 'first_name': 'Admin', 'last_name': 'User'},
            {'username': 'manager1', 'email': 'manager1@omnistore.com', 'role': 'manager', 'first_name': 'John', 'last_name': 'Manager'},
            {'username': 'manager2', 'email': 'manager2@omnistore.com', 'role': 'manager', 'first_name': 'Sarah', 'last_name': 'Wilson'},
            {'username': 'staff1', 'email': 'staff1@omnistore.com', 'role': 'staff', 'first_name': 'Mike', 'last_name': 'Johnson'},
            {'username': 'staff2', 'email': 'staff2@omnistore.com', 'role': 'staff', 'first_name': 'Emily', 'last_name': 'Davis'},
            {'username': 'staff3', 'email': 'staff3@omnistore.com', 'role': 'staff', 'first_name': 'Chris', 'last_name': 'Brown'},
            {'username': 'customer1', 'email': 'alice.smith@email.com', 'role': 'staff', 'first_name': 'Alice', 'last_name': 'Smith'},
            {'username': 'customer2', 'email': 'bob.wilson@email.com', 'role': 'staff', 'first_name': 'Bob', 'last_name': 'Wilson'},
            {'username': 'customer3', 'email': 'carol.jones@email.com', 'role': 'staff', 'first_name': 'Carol', 'last_name': 'Jones'},
            {'username': 'customer4', 'email': 'david.lee@email.com', 'role': 'staff', 'first_name': 'David', 'last_name': 'Lee'},
            {'username': 'customer5', 'email': 'eve.miller@email.com', 'role': 'staff', 'first_name': 'Eve', 'last_name': 'Miller'},
        ]

        users = []
        for data in users_data:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data['email'],
                    'role': data['role'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            users.append(user)
        return users

    def create_categories(self):
        categories_data = [
            {'name': 'Electronics', 'description': 'Gadgets, devices, and electronic accessories'},
            {'name': 'Clothing', 'description': 'Apparel and fashion items'},
            {'name': 'Home & Garden', 'description': 'Furniture, decor, and garden supplies'},
            {'name': 'Sports & Outdoors', 'description': 'Athletic gear and outdoor equipment'},
            {'name': 'Books & Media', 'description': 'Books, music, movies, and games'},
            {'name': 'Health & Beauty', 'description': 'Personal care and beauty products'},
            {'name': 'Toys & Games', 'description': 'Kids toys and board games'},
            {'name': 'Food & Beverages', 'description': 'Food items and drinks'},
        ]

        categories = []
        for data in categories_data:
            cat, _ = Category.objects.get_or_create(name=data['name'], defaults={'description': data['description']})
            categories.append(cat)

        # Create subcategories
        subcategories_data = [
            {'name': 'Smartphones', 'parent': 'Electronics'},
            {'name': 'Laptops', 'parent': 'Electronics'},
            {'name': 'Headphones', 'parent': 'Electronics'},
            {'name': 'Men\'s Clothing', 'parent': 'Clothing'},
            {'name': 'Women\'s Clothing', 'parent': 'Clothing'},
            {'name': 'Kids\' Clothing', 'parent': 'Clothing'},
            {'name': 'Kitchen Appliances', 'parent': 'Home & Garden'},
            {'name': 'Furniture', 'parent': 'Home & Garden'},
            {'name': 'Fitness Equipment', 'parent': 'Sports & Outdoors'},
            {'name': 'Camping Gear', 'parent': 'Sports & Outdoors'},
            {'name': 'Fiction', 'parent': 'Books & Media'},
            {'name': 'Non-Fiction', 'parent': 'Books & Media'},
            {'name': 'Skincare', 'parent': 'Health & Beauty'},
            {'name': 'Makeup', 'parent': 'Health & Beauty'},
        ]

        for data in subcategories_data:
            parent = Category.objects.get(name=data['parent'])
            cat, _ = Category.objects.get_or_create(
                name=data['name'],
                defaults={'parent': parent, 'description': f'{data["name"]} products'}
            )
            categories.append(cat)

        return categories

    def create_products(self, categories):
        products_data = [
            # Electronics
            {'name': 'iPhone 15 Pro Max', 'category': 'Smartphones', 'base_price': 1199.00, 'status': 'live'},
            {'name': 'Samsung Galaxy S24 Ultra', 'category': 'Smartphones', 'base_price': 1299.00, 'status': 'live'},
            {'name': 'Google Pixel 8 Pro', 'category': 'Smartphones', 'base_price': 999.00, 'status': 'live'},
            {'name': 'MacBook Pro 16"', 'category': 'Laptops', 'base_price': 2499.00, 'status': 'live'},
            {'name': 'Dell XPS 15', 'category': 'Laptops', 'base_price': 1799.00, 'status': 'live'},
            {'name': 'ThinkPad X1 Carbon', 'category': 'Laptops', 'base_price': 1649.00, 'status': 'live'},
            {'name': 'Sony WH-1000XM5', 'category': 'Headphones', 'base_price': 399.00, 'status': 'live'},
            {'name': 'AirPods Pro 2', 'category': 'Headphones', 'base_price': 249.00, 'status': 'live'},
            {'name': 'Bose QuietComfort Ultra', 'category': 'Headphones', 'base_price': 429.00, 'status': 'live'},
            # Clothing
            {'name': 'Classic Fit Cotton T-Shirt', 'category': 'Men\'s Clothing', 'base_price': 29.99, 'status': 'live'},
            {'name': 'Slim Fit Jeans', 'category': 'Men\'s Clothing', 'base_price': 79.99, 'status': 'live'},
            {'name': 'Casual Blazer', 'category': 'Men\'s Clothing', 'base_price': 149.99, 'status': 'live'},
            {'name': 'Summer Dress', 'category': 'Women\'s Clothing', 'base_price': 89.99, 'status': 'live'},
            {'name': 'High Waist Jeans', 'category': 'Women\'s Clothing', 'base_price': 69.99, 'status': 'live'},
            {'name': 'Silk Blouse', 'category': 'Women\'s Clothing', 'base_price': 119.99, 'status': 'live'},
            {'name': 'Kids Hoodie', 'category': 'Kids\' Clothing', 'base_price': 39.99, 'status': 'live'},
            {'name': 'Kids Rain Jacket', 'category': 'Kids\' Clothing', 'base_price': 49.99, 'status': 'live'},
            # Home & Garden
            {'name': 'Air Fryer Pro 5L', 'category': 'Kitchen Appliances', 'base_price': 129.99, 'status': 'live'},
            {'name': 'Instant Pot Duo 7-in-1', 'category': 'Kitchen Appliances', 'base_price': 99.99, 'status': 'live'},
            {'name': 'Coffee Maker Deluxe', 'category': 'Kitchen Appliances', 'base_price': 79.99, 'status': 'live'},
            {'name': 'Ergonomic Office Chair', 'category': 'Furniture', 'base_price': 299.99, 'status': 'live'},
            {'name': 'Standing Desk', 'category': 'Furniture', 'base_price': 449.99, 'status': 'live'},
            {'name': 'Bookshelf 5-Tier', 'category': 'Furniture', 'base_price': 159.99, 'status': 'live'},
            # Sports & Outdoors
            {'name': 'Yoga Mat Premium', 'category': 'Fitness Equipment', 'base_price': 49.99, 'status': 'live'},
            {'name': 'Dumbbell Set 20kg', 'category': 'Fitness Equipment', 'base_price': 89.99, 'status': 'live'},
            {'name': 'Treadmill Foldable', 'category': 'Fitness Equipment', 'base_price': 599.99, 'status': 'live'},
            {'name': 'Camping Tent 4-Person', 'category': 'Camping Gear', 'base_price': 199.99, 'status': 'live'},
            {'name': 'Hiking Backpack 50L', 'category': 'Camping Gear', 'base_price': 129.99, 'status': 'live'},
            {'name': 'Sleeping Bag -20C', 'category': 'Camping Gear', 'base_price': 149.99, 'status': 'live'},
            # Books & Media
            {'name': 'The Art of Programming', 'category': 'Fiction', 'base_price': 24.99, 'status': 'live'},
            {'name': 'Midnight Mystery', 'category': 'Fiction', 'base_price': 19.99, 'status': 'live'},
            {'name': 'Cooking Masterclass', 'category': 'Non-Fiction', 'base_price': 34.99, 'status': 'live'},
            {'name': 'History of Science', 'category': 'Non-Fiction', 'base_price': 29.99, 'status': 'live'},
            # Health & Beauty
            {'name': 'Vitamin C Serum', 'category': 'Skincare', 'base_price': 45.99, 'status': 'live'},
            {'name': 'Anti-Aging Cream', 'category': 'Skincare', 'base_price': 79.99, 'status': 'live'},
            {'name': 'Moisturizing Lotion', 'category': 'Skincare', 'base_price': 29.99, 'status': 'live'},
            {'name': 'Lipstick Collection', 'category': 'Makeup', 'base_price': 59.99, 'status': 'live'},
            {'name': 'Foundation Palette', 'category': 'Makeup', 'base_price': 69.99, 'status': 'live'},
            {'name': 'Mascara Pro', 'category': 'Makeup', 'base_price': 24.99, 'status': 'live'},
            # Draft products
            {'name': 'Smart Watch X', 'category': 'Electronics', 'base_price': 399.00, 'status': 'draft'},
            {'name': 'Winter Jacket', 'category': 'Men\'s Clothing', 'base_price': 199.99, 'status': 'draft'},
            # Archived products
            {'name': 'Old Smartphone', 'category': 'Smartphones', 'base_price': 599.00, 'status': 'archived'},
        ]

        products = []
        for data in products_data:
            cat = next((c for c in categories if c.name == data['category']), None)
            prod, created = Product.objects.get_or_create(
                name=data['name'],
                defaults={
                    'category': cat,
                    'base_price': data['base_price'],
                    'status': data['status'],
                    'description': f'High quality {data["name"]} for everyday use.'
                }
            )
            products.append(prod)
        return products

    def create_variants(self, products):
        colors = ['Black', 'White', 'Red', 'Blue', 'Green', 'Silver', 'Gold', 'Pink']
        sizes = ['S', 'M', 'L', 'XL', 'XXL']
        variants = []

        for product in products:
            if product.status == 'live':
                # Electronics - different storage options
                if product.category and product.category.name in ['Smartphones', 'Laptops']:
                    for storage in ['128GB', '256GB', '512GB', '1TB']:
                        sku = f"{product.slug[:8].upper()}-{storage.replace('GB','')}"
                        variant, _ = ProductVariant.objects.get_or_create(
                            sku=sku,
                            defaults={
                                'product': product,
                                'price_override': product.base_price + (int(storage.replace('GB','')) * 0.5) if 'TB' not in storage else product.base_price + 200,
                            }
                        )
                        variants.append(variant)
                # Clothing - different colors and sizes
                elif product.category and product.category.name in ["Men's Clothing", "Women's Clothing", "Kids' Clothing"]:
                    for color in random.sample(colors, 3):
                        for size in random.sample(sizes, 3):
                            sku = f"{product.slug[:6].upper()}-{color[:2].upper()}-{size}"
                            price_override = product.base_price + random.uniform(5, 15) if size in ['XL', 'XXL'] else None
                            variant, _ = ProductVariant.objects.get_or_create(
                                sku=sku,
                                defaults={
                                    'product': product,
                                    'color': color,
                                    'size': size,
                                    'price_override': round(price_override, 2) if price_override else None,
                                }
                            )
                            variants.append(variant)
                # Generic variants
                else:
                    for color in random.sample(colors, 2):
                        sku = f"{product.slug[:8].upper()}-{color[:2].upper()}"
                        variant, _ = ProductVariant.objects.get_or_create(
                            sku=sku,
                            defaults={'product': product, 'color': color}
                        )
                        variants.append(variant)

        return variants

    def create_stock_items(self, variants):
        locations = ['Warehouse A', 'Warehouse B', 'Warehouse C', 'Store Front', 'Distribution Center']
        for variant in variants:
            location = random.choice(locations)
            StockItem.objects.get_or_create(
                variant=variant,
                location=location,
                defaults={
                    'quantity': random.randint(0, 500),
                    'low_stock_threshold': random.randint(5, 20),
                }
            )
            # Add a second stock location for some items
            if random.random() > 0.6:
                other_locations = [l for l in locations if l != location]
                StockItem.objects.get_or_create(
                    variant=variant,
                    location=random.choice(other_locations),
                    defaults={
                        'quantity': random.randint(0, 200),
                        'low_stock_threshold': random.randint(5, 20),
                    }
                )

    def create_discounts(self, categories, products):
        now = timezone.now()

        discounts_data = [
            {
                'code': 'SUMMER20',
                'discount_type': 'percentage',
                'value': 20,
                'active_from': now - timedelta(days=10),
                'active_until': now + timedelta(days=30),
                'is_active': True,
                'usage_limit': 100,
            },
            {
                'code': 'FLAT50',
                'discount_type': 'flat',
                'value': 50,
                'active_from': now - timedelta(days=5),
                'active_until': now + timedelta(days=25),
                'is_active': True,
                'usage_limit': 50,
            },
            {
                'code': 'ELECTRONICS15',
                'discount_type': 'percentage',
                'value': 15,
                'active_from': now - timedelta(days=3),
                'active_until': now + timedelta(days=60),
                'is_active': True,
                'usage_limit': None,
            },
            {
                'code': 'NEWUSER10',
                'discount_type': 'flat',
                'value': 10,
                'active_from': now - timedelta(days=1),
                'active_until': now + timedelta(days=365),
                'is_active': True,
                'usage_limit': 1,
            },
            {
                'code': 'FLASH25',
                'discount_type': 'percentage',
                'value': 25,
                'active_from': now - timedelta(hours=12),
                'active_until': now + timedelta(hours=36),
                'is_active': True,
                'usage_limit': 20,
            },
            {
                'code': 'EXPIRED50',
                'discount_type': 'flat',
                'value': 50,
                'active_from': now - timedelta(days=30),
                'active_until': now - timedelta(days=1),
                'is_active': True,
                'usage_limit': None,
            },
        ]

        discounts = []
        for data in discounts_data:
            discount, _ = Discount.objects.get_or_create(
                code=data['code'],
                defaults=data
            )
            discounts.append(discount)

        # Add category and product associations
        electronics_cat = next((c for c in categories if c.name == 'Electronics'), None)
        smartphones_cat = next((c for c in categories if c.name == 'Smartphones'), None)

        if electronics_cat and discounts[2]:  # ELECTRONICS15
            discounts[2].categories.add(electronics_cat)

        if smartphones_cat and discounts[3]:  # NEWUSER10
            discounts[3].categories.add(smartphones_cat)

        # Create discount rules
        for discount in discounts[:4]:  # First 4 discounts
            DiscountRule.objects.get_or_create(
                discount=discount,
                defaults={
                    'min_order_value': random.choice([None, 50, 100, 200]),
                    'limit_per_user': random.choice([None, 1, 3, 5]),
                }
            )

        return discounts

    def create_orders(self, users, variants):
        statuses = ['pending', 'confirmed', 'paid', 'shipped', 'delivered', 'cancelled', 'refunded']
        orders = []

        # Get customers only (non-staff users for customer field)
        customers = [u for u in users if u.username.startswith('customer')]

        for i in range(50):
            order_date = timezone.now() - timedelta(days=random.randint(0, 90))
            status = random.choice(statuses)
            customer = random.choice(customers) if random.random() > 0.2 else None

            order = Order.objects.create(
                order_id=f'ORD-{2024}{random.randint(100000, 999999)}',
                customer=customer,
                customer_email=customer.email if customer else f'guest{random.randint(1,100)}@guest.com',
                total_price=random.uniform(25, 1500),
                status=status,
                shipping_address=f'{random.randint(1,999)} {random.choice(["Main", "Oak", "Maple", "Cedar"])} St, City, State {random.randint(10000, 99999)}',
                notes='Order placed online' if random.random() > 0.7 else '',
            )
            orders.append(order)

            # Create order items (1-5 items per order)
            num_items = random.randint(1, 5)
            order_variants = random.sample(variants, min(num_items, len(variants)))

            for variant in order_variants:
                OrderItem.objects.create(
                    order=order,
                    product_name=variant.product.name,
                    product_price=variant.price,
                    quantity=random.randint(1, 4),
                    variant=variant,
                )

            # Create status history
            OrderStatusHistory.objects.create(
                order=order,
                status=status,
                notes=f'Order {status}',
                created_by=users[0] if random.random() > 0.3 else None,
            )

            # Add some historical status changes for delivered/older orders
            if status in ['delivered', 'shipped'] and random.random() > 0.5:
                OrderStatusHistory.objects.create(
                    order=order,
                    status='pending',
                    notes='Order placed',
                    created_by=None,
                )
                OrderStatusHistory.objects.create(
                    order=order,
                    status='confirmed',
                    notes='Payment confirmed',
                    created_by=random.choice(users[:3]),
                )
                if status == 'shipped':
                    OrderStatusHistory.objects.create(
                        order=order,
                        status='shipped',
                        notes='Order shipped',
                        created_by=random.choice(users[:3]),
                    )

        return orders
