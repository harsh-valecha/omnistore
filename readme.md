Project Specification: "OmniStore Admin & Engine" (Django Stack)
This is a comprehensive Headless E-Commerce Management System built with a Django monolithic architecture. It uses Django Templates for the frontend, PostgreSQL (or SQLite) for the database, and Vanilla JS for dynamic UI interactions.
1. Project Architecture
 * Backend: Django 5.x (Python)
 * Frontend: Django Template Language (DTL), Tailwind CSS (or Bootstrap 5), and Vanilla JavaScript.
 * Database: PostgreSQL (Recommended for relational integrity between Products, Orders, and Users).
 * Static/Media: Django staticfiles and media root for product imagery.
2. Module Breakdown
Module A: Product & Inventory Engine (catalog app)
 * Models: * Category: Recursive relationship (self-referential) for sub-categories.
   * Product: Fields for name, slug, description, base price, and status (Draft/Live/Archived).
   * ProductVariant: Links to Product; tracks specific SKU, size, color, and specific price overrides.
   * StockItem: Tracks quantity, low-stock thresholds, and location (e.g., "Warehouse A").
 * Frontend Features:
   * Dynamic variant adder (JS-driven form to add rows for sizes/colors).
   * Image drag-and-drop uploader.
Module B: Rules-Based Discount Engine (promotions app)
 * Models:
   * Discount: Fields for code, type (Percentage vs. Flat), value, and active dates.
   * DiscountRule: Logic-based constraints (e.g., min_order_value, limit_per_user, or category_specific).
 * Frontend Features:
   * Searchable dropdowns to link discounts to specific products or categories.
Module C: Order State Machine (sales app)
 * Models:
   * Order: Unique Order ID, Customer Email/User, Total Price, and Status.
   * OrderItem: Snapshot of the product name and price at the time of purchase (to prevent history changes if product prices update later).
   * OrderStatusHistory: A log tracking status changes (e.g., Pending \rightarrow Paid).
 * Frontend Features:
   * Order Detail View: A timeline visualization of the status history.
   * Status Update buttons (e.g., "Mark as Shipped") that trigger backend state transitions.
Module D: Custom RBAC (identity app)
 * Implementation: Utilize Django’s built-in Group and Permission system.
 * Roles:
   * Admin: Access to /admin/ and all dashboard views.
   * Manager: Access to Product and Discount modules only.
   * Staff: Access to Order and Inventory modules only.
 * Frontend Features:
   * Sidebar navigation that conditionally hides links based on user permissions ({% if perms.sales.view_order %}).
3. Core Database Schema (Key Relationships)
| Table | Relation Type | Target Table |
|---|---|---|
| Product | ForeignKey | Category |
| ProductVariant | ForeignKey | Product |
| OrderItem | ForeignKey | Order & ProductVariant |
| Discount | ManyToMany | Category (Optional scope) |
4. Key Functional Requirements for the Agent
 * Slug Generation: Automatically generate URL slugs from product names using signals or overriding save().
 * Calculated Properties: Use Django @property decorators to calculate "Final Price" (Base Price + Variant Premium - active Discounts).
 * Search & Filter: Implement a robust filtering system in the dashboard using Q objects for multi-field searching (SKU, Name, Category).
 * Form Validation: Custom Django Clean methods to ensure stock cannot be negative and discount codes are unique.
5. Directory Structure for the Agent
omnistore_root/
├── manage.py
├── core/ # Project Settings & WSGI
├── catalog/ # Products, Variants, Categories
├── sales/ # Orders, OrderItems, Status Tracking
├── promotions/ # Discounts & Coupons
├── identity/ # Custom User Profiles & RBAC
├── static/ # CSS, JS, Images
└── templates/ # Base, Dashboard, and Module-specific HTML

