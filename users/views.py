from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.db import IntegrityError
from .models import CustomUser, Profile

# Create your views here.
User = get_user_model()

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
    errors = {}
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")

        if not username:
            errors['username'] = "Please enter a username."
        if not email:
            errors['email'] = "Please enter an email"
        if not password:
            errors['password'] = "Please enter a password."
        if password != confirmation:
            errors['confirmation'] = "Passwords do not match."

        # Check for duplicates
        if User.objects.filter(username=username).exists():
            errors['username'] = "Username already taken."
        if User.objects.filter(email=email).exists():
            errors['email'] = "Email already in use."
        
        #Create user if no errors
        if not errors:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('index')
    
    return render(request, 'registration/register.html', {
        'errors': errors
    })
    

def profile(request, profile_id):
    profile_info = Profile.objects.filter(id=profile_id).all()
    return render(request, 'profile.html', {
        'profile_info': profile_info
    })