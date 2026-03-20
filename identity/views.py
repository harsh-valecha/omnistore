from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User


@login_required
def dashboard(request):
    """Identity module dashboard"""
    return render(request, 'identity/dashboard.html')


def user_login(request):
    """User login view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid credentials')
    return render(request, 'identity/login.html')


def user_logout(request):
    """User logout view"""
    logout(request)
    return redirect('identity:login')


@login_required
def user_list(request):
    """List all users (admin only)"""
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'identity/user_list.html', {'users': users})
