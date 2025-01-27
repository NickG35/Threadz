from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError
from .models import User, Profile

# Create your views here.

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        errors = {}

        if not username:
            errors['username'] = 'Enter a valid username'
        if not password:
            errors['password'] = 'Enter a password'

        if not errors:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('index')
                else:
                    errors['invalid_credentials'] = 'Invalid username or password'
        
        return render(request, 'registration/login.html', {
            'errors': errors
        })
    
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

def profile(request, profile_id):
    profile_info = Profile.objects.filter(id=profile_id).all()
    return render(request, 'profile.html', {
        'profile_info': profile_info
    })