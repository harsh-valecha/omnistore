from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Discount, DiscountRule


@login_required
def dashboard(request):
    """Promotions module dashboard"""
    active_discounts = Discount.objects.filter(is_active=True)[:10]
    context = {'active_discounts': active_discounts}
    return render(request, 'promotions/dashboard.html', context)


@login_required
def discount_list(request):
    """List all discounts"""
    query = request.GET.get('q', '')
    discounts = Discount.objects.all().order_by('-created_at')
    if query:
        discounts = discounts.filter(code__icontains=query).distinct()
    context = {'discounts': discounts, 'query': query}
    return render(request, 'promotions/discount_list.html', context)


@login_required
def discount_detail(request, pk):
    """Discount detail with rules"""
    discount = get_object_or_404(Discount, pk=pk)
    rules = discount.rules.all()
    context = {'discount': discount, 'rules': rules}
    return render(request, 'promotions/discount_detail.html', context)
