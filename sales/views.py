from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Order, OrderItem, OrderStatusHistory


@login_required
def dashboard(request):
    """Sales module dashboard"""
    recent_orders = Order.objects.all()[:10]
    context = {'recent_orders': recent_orders}
    return render(request, 'sales/dashboard.html', context)


@login_required
def order_list(request):
    """List all orders with search/filter"""
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')

    orders = Order.objects.all().order_by('-created_at')
    if query:
        orders = orders.filter(
            Q(order_id__icontains=query) |
            Q(customer_email__icontains=query)
        ).distinct()
    if status:
        orders = orders.filter(status=status)

    context = {'orders': orders, 'query': query, 'status': status}
    return render(request, 'sales/order_list.html', context)


@login_required
def order_detail(request, pk):
    """Order detail with status history timeline"""
    order = get_object_or_404(Order, pk=pk)
    items = order.items.all()
    history = order.status_history.all().order_by('-created_at')
    context = {'order': order, 'items': items, 'history': history}
    return render(request, 'sales/order_detail.html', context)


@login_required
def update_order_status(request, pk):
    """Update order status"""
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        notes = request.POST.get('notes', '')
        if new_status:
            order.status = new_status
            order.save()
            OrderStatusHistory.objects.create(
                order=order,
                status=new_status,
                notes=notes,
                created_by=request.user
            )
        return redirect('sales:order_detail', pk=pk)
    return redirect('sales:order_list')
