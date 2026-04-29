from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import SignUpForm
from orders.utils import merge_cart

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    next_url = request.GET.get('next') or request.POST.get('next') or 'home'
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            guest_session_key = request.session.session_key
            login(request, user)
            merge_cart(request, user, guest_session_key=guest_session_key)
            messages.success(request, f"Welcome to Khaja Kham! Your account has been created.")
            return redirect(next_url)
        else:
            messages.error(request, "Registration failed. Please check the errors below.")
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form, 'next': request.GET.get('next', '')})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    next_url = request.GET.get('next') or request.POST.get('next') or 'home'
    if request.method == 'POST':
        identifier = request.POST.get('username') 
        password = request.POST.get('password')
        form = AuthenticationForm(request, data=request.POST)
        
        from users.models import User
        auth_username = identifier
        if '@' in identifier:
            # Look up user by email if identifier looks like an email
            user_obj = User.objects.filter(email=identifier).first()
            if user_obj:
                auth_username = user_obj.username

        user = authenticate(username=auth_username, password=password)
        
        if user is not None:
            guest_session_key = request.session.session_key
            login(request, user)
            merge_cart(request, user, guest_session_key=guest_session_key)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect(next_url)
        else:
            messages.error(request, "Invalid email/username or password. Please try again.")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form, 'next': request.GET.get('next', '')})
