from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import SignUpForm
from orders.utils import merge_cart

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            merge_cart(request, user)
            messages.success(request, f"Welcome to Khaja Kham, {user.username}! Your account has been created successfully.")
            return redirect('home')
        else:
            messages.error(request, "Registration failed. Please check the errors below.")
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        identifier = request.POST.get('username') # This will be either email or username
        password = request.POST.get('password')
        
        # If identifier looks like email, try to find user by email
        from users.models import User
        user_obj = None
        if '@' in identifier:
            try:
                user_obj = User.objects.get(email=identifier)
                auth_username = user_obj.username
            except User.DoesNotExist:
                auth_username = identifier # Fallback, maybe it's a username with @
        else:
            auth_username = identifier

        user = authenticate(username=auth_username, password=password)
        
        if user is not None:
            login(request, user)
            merge_cart(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid email/username or password. Please try again.")
            form = AuthenticationForm() # Return empty form or keep data
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})
