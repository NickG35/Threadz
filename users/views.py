from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout, get_user_model
from .models import Profile
from orders.models import Order
from products.models import Product

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
        'hidden': True,
        'profile_info': profile_info
    })

def update_password(request, profile_id):
    profile_info = Profile.objects.filter(id=profile_id).all()  # Keep profile info
    if request.method == 'POST':
        errors = {}

        currentPassword = request.POST.get("current_password")
        newPassword = request.POST.get("new_password")

        profile_user = Profile.objects.get(id=profile_id)
        user = profile_user.user

        if not currentPassword:
            errors['currentPassword'] = "Current password is required"
        elif not check_password(currentPassword, user.password):
            errors['currentPassword'] = "Current password is incorrect."

        if not newPassword:
            errors['newPassword'] = "New password is required"
        elif check_password(newPassword, user.password):
            errors['newPassword'] = "New password must be different from the old password."

        if errors:
            return render(request, "change_password.html", {
                "profile_info": profile_info,
                "errors": errors  # Pass errors to the template
            })

        user.set_password(newPassword)
        user.save()
        authenticated_user = authenticate(username=user.username, password=newPassword)
        if authenticated_user:
            login(request, authenticated_user)
            
        messages.success(request, "Your password has been successfully updated!", extra_tags="password")
        return redirect('update_password', profile_id=profile_id)

    return render(request, "change_password.html", {
        "profile_info": profile_info,
        "hidden": True
    })

def update_user(request, profile_id):
    profile_info = Profile.objects.filter(id=profile_id).all()
    if request.method == 'POST':
        errors = {}
        userName = request.POST.get("username")
        email = request.POST.get("email")

        profile_user = Profile.objects.get(id=profile_id)
        user = profile_user.user

        current_username = user.username
        current_email = user.email

        if not userName:
            errors['userName'] = "Username is required."
        if userName != current_username and User.objects.filter(username=userName).exclude(id=profile_id).exists():
            errors['userName'] = "Username taken by another user."
        
        if not email:
            errors['email'] = "email is required"
        if email != current_email and User.objects.filter(email=email).exclude(id=profile_id).exists():
            errors['userName'] = "Email already in use."

        if errors:
            return render(request, "account_details.html", {
                "profile_info": profile_info,
                "errors": errors,  # Pass errors to the template
            })
        
        user.username = userName
        user.email = email
        user.save()
        
        messages.success(request, "Your user information has been updated!", extra_tags="user")
        return redirect('update_user', profile_id=profile_id)
    
    return render(request, "account_details.html", {
        "profile_info": profile_info,
        "hidden": True
    })

def my_clothes(request, profile_id):
    profile_products = Product.objects.filter(created_by=profile_id).all()
    return render(request, 'my_clothes.html', {
        'profile_products': profile_products,
        "hidden": True
    })

def my_orders(request, profile_id):
    profile_orders = Order.objects.filter(user=profile_id).order_by('-purchase_date').all()
    return render(request, 'my_orders.html', {
        'orders': profile_orders,
        "hidden": True
    })