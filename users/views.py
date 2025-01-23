from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError
from .models import User

# Create your views here.

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return redirect('login')
    else:
        return render(request, 'registration/login.html')

def logout_user(request):
    logout(request)
    return redirect('index')

def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")
        errors = {}

        if not username:
            errors['username'] = "Please enter a username."
        if not password:
            errors['password'] = "Please enter a password."
        if password != confirmation:
            errors['confirmation'] = "Passwords do not match."
        if not errors:
            try:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                login(request, user)
                return redirect('index')
            except IntegrityError:
                errors['username'] = "Username already taken."
    
        return render(request, 'registration/register.html', {
            'errors': errors
        })
    
    return render(request, "registration/register.html")

def profile(request):
    return render(request, 'profile.html')