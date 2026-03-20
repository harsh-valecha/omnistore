from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from .models import Category, Product, ProductVariant, StockItem


@login_required
def dashboard(request):
    """Catalog module dashboard"""
    products = Product.objects.all()[:10]
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'catalog/dashboard.html', context)


@login_required
def product_list(request):
    """List all products with search/filter"""
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')

    products = Product.objects.all()
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(slug__icontains=query) |
            Q(variants__sku__icontains=query)
        ).distinct()
    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'query': query,
    }
    return render(request, 'catalog/product_list.html', context)


@login_required
def product_detail(request, pk):
    """Product detail view"""
    product = get_object_or_404(Product, pk=pk)
    variants = product.variants.all()
    context = {'product': product, 'variants': variants}
    return render(request, 'catalog/product_detail.html', context)


@login_required
def category_list(request):
    """List all categories"""
    categories = Category.objects.filter(parent__isnull=True).prefetch_related('children')
    return render(request, 'catalog/category_list.html', {'categories': categories})
