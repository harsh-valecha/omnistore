# OmniStore Admin & Engine - User Guide

A comprehensive Headless E-Commerce Management System built with Django.

## Quick Start

### 1. Start the Server

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000 in your browser.

### 2. Login

**URL:** http://127.0.0.1:8000/identity/login/

**Default Admin Credentials:**
- Username: `admin`
- Password: `admin123`

### 3. Dashboard

After login, you'll see the main dashboard with navigation cards for each module:
- **Catalog** - Products, Variants, Categories, Inventory
- **Sales** - Orders, Status Management
- **Promotions** - Discounts & Coupons
- **Users** - User Management

---

## Module Guide

### Module A: Catalog (Products & Inventory)

**URL:** `/catalog/`

Manage your product catalog with categories, variants, and stock tracking.

#### Features:
- **Product List** - View all products with search by name, slug, or SKU
- **Product Detail** - View product info and all associated variants
- **Category List** - Hierarchical category management (parent/child categories)

#### Key Concepts:

| Concept | Description |
|---------|-------------|
| **Category** | Groups products; supports sub-categories via parent relationship |
| **Product** | Main product entity with name, slug, base price, and status (Draft/Live/Archived) |
| **ProductVariant** | Specific SKU with size/color options and price overrides |
| **StockItem** | Inventory tracking per variant with low-stock alerts |

#### Product Statuses:
- `draft` - Not visible to customers
- `live` - Active and visible
- `archived` - Hidden and no longer sold

#### Navigation:
- `/catalog/dashboard/` - Overview with recent products
- `/catalog/products/` - Full product list with search
- `/catalog/products/<id>/` - Product detail view
- `/catalog/categories/` - Category management

---

### Module B: Sales (Orders & State Machine)

**URL:** `/sales/`

Process and track orders through their lifecycle.

#### Features:
- **Order List** - Search by order ID or customer email, filter by status
- **Order Detail** - Full order info with status history timeline
- **Status Updates** - Transition orders through the state machine

#### Order Statuses:
```
pending → confirmed → paid → shipped → delivered
                ↓
            cancelled → refunded
```

#### Navigation:
- `/sales/dashboard/` - Recent orders overview
- `/sales/orders/` - All orders with search/filter
- `/sales/orders/<id>/` - Order detail with timeline
- `/sales/orders/<id>/update-status/` - POST endpoint for status changes

#### Status History:
Every status change is logged with:
- New status
- Timestamp
- Optional notes
- User who made the change

---

### Module C: Promotions (Discounts & Coupons)

**URL:** `/promotions/`

Create and manage discount campaigns.

#### Discount Types:
| Type | Description |
|------|-------------|
| `percentage` | Percentage off (e.g., 20% off) |
| `flat` | Fixed amount off (e.g., $10 off) |

#### Features:
- **Discount List** - All discounts with search
- **Discount Detail** - Full info with associated rules
- **Discount Rules** - Constraints like minimum order value, usage limits, category restrictions

#### Validation:
- Percentage discounts cannot exceed 100%
- Discounts check validity based on:
  - `is_active` flag
  - `active_from` and `active_until` dates
  - `usage_limit` vs `usage_count`

#### Navigation:
- `/promotions/dashboard/` - Active discounts overview
- `/promotions/discounts/` - All discounts
- `/promotions/discounts/<id>/` - Discount detail with rules

---

### Module D: Identity (Users & RBAC)

**URL:** `/identity/`

Manage users and role-based access control.

#### User Roles:

| Role | Permissions |
|------|-------------|
| **Admin** | Full access to all modules including `/admin/` |
| **Manager** | Catalog and Promotions modules only |
| **Staff** | Sales module only |

#### Custom Permissions:
- `view_all_orders` - See all orders regardless of status
- `manage_inventory` - Edit stock and product variants
- `manage_discounts` - Create/edit promotional campaigns

#### Navigation:
- `/identity/login/` - User login
- `/identity/logout/` - User logout
- `/identity/dashboard/` - Current user info
- `/identity/users/` - User management (admin only)

---

## Search & Filtering

Each list view supports search and filtering:

### Products (`/catalog/products/`)
- **Search:** Name, slug, or SKU
- **Filter:** By category

### Orders (`/sales/orders/`)
- **Search:** Order ID or customer email
- **Filter:** By status (pending, confirmed, paid, shipped, delivered, cancelled, refunded)

### Discounts (`/promotions/discounts/`)
- **Search:** Discount code

---

## Admin Interface

Full Django admin access at `/admin/`

Access to:
- All models with CRUD operations
- Group and permission management
- User management
- Database management

---

## API Endpoints Summary

| Module | Endpoint | Method | Description |
|--------|----------|--------|-------------|
| Catalog | `/catalog/dashboard/` | GET | Dashboard |
| Catalog | `/catalog/products/` | GET | Product list |
| Catalog | `/catalog/products/<id>/` | GET | Product detail |
| Catalog | `/catalog/categories/` | GET | Category list |
| Sales | `/sales/dashboard/` | GET | Dashboard |
| Sales | `/sales/orders/` | GET | Order list |
| Sales | `/sales/orders/<id>/` | GET | Order detail |
| Sales | `/sales/orders/<id>/update-status/` | POST | Update status |
| Promotions | `/promotions/dashboard/` | GET | Dashboard |
| Promotions | `/promotions/discounts/` | GET | Discount list |
| Promotions | `/promotions/discounts/<id>/` | GET | Discount detail |
| Identity | `/identity/login/` | GET/POST | Login |
| Identity | `/identity/logout/` | GET | Logout |
| Identity | `/identity/users/` | GET | User list |

---

## Common Tasks

### Create a New Product
1. Go to `/catalog/products/`
2. (Admin) Use Django admin at `/admin/catalog/product/add/`
3. Set name, slug, base price, category, and status

### Add Variant to Product
1. Go to Django admin `/admin/`
2. Navigate to Catalog > Product Variants
3. Add variant with SKU, size, color, and optional price override

### Process an Order
1. Go to `/sales/orders/`
2. Click on order ID
3. Use the status update form to transition:
   - Pending → Confirmed → Paid → Shipped → Delivered

### Create a Discount
1. Go to Django admin `/admin/promotions/`
2. Add Discount with code, type, value, and date range
3. Optionally add DiscountRule for constraints

### Manage Users & Roles
1. Go to `/admin/`
2. Navigate to Identity > Users
3. Set role: Admin, Manager, or Staff
4. Assign to Groups for permissions

---

## Project Structure

```
omnistore/
├── manage.py
├── core/               # Django settings & URLs
│   ├── settings.py
│   └── urls.py
├── catalog/            # Module A: Products & Inventory
│   ├── models.py       # Category, Product, ProductVariant, StockItem
│   ├── views.py
│   └── urls.py
├── sales/              # Module B: Orders & State Machine
│   ├── models.py       # Order, OrderItem, OrderStatusHistory
│   ├── views.py
│   └── urls.py
├── promotions/         # Module C: Discounts
│   ├── models.py       # Discount, DiscountRule
│   ├── views.py
│   └── urls.py
├── identity/           # Module D: Users & RBAC
│   ├── models.py       # User (custom)
│   ├── views.py
│   └── urls.py
├── templates/          # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   └── <module>/
└── static/             # CSS, JS, images
```

---

## Tech Stack

- **Backend:** Django 6.x
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **Frontend:** Bootstrap 5, Vanilla JavaScript
- **Auth:** Django built-in with custom User model

---
## Dummy data details - 
for all the users except admin have password as 'password123'

## Support

For issues or questions, check:
1. Django console for error messages
2. `/admin/` for data validation
3. Server logs for runtime errors
