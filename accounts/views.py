# Create your views here.
import re
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import Account
from django.contrib import messages
from django.db import models

def store_home(request):
    return render(request, 'index.html')

def sign_in(request):
    
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            email = Account.objects.get(email=email)
        except Account.DoesNotExist:
            messages.error(request, 'Your account does not register with us!')
            return render(request, 'sign-in.html')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
            #return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, 'Username OR Password is incorrect')

    return render(request, 'sign-in.html')

def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect("home")


def is_valid_password(password):
    # Password complexity: At least 8 characters including one uppercase, one lowercase, one digit, and one special character
    return bool(re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password))

def is_valid_phone_number(phone_number):
    # Phone number validation: Allow digits and '+' symbol only and require a specific length (adjust as needed)
    pattern = r'^\+\d{0,12}$'
    return bool(re.match(pattern, phone_number))

def sign_up(request):

    if request.user.is_authenticated:
        return redirect("home")
     
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        errors = []

        if not (username and first_name and last_name and email and phone_number and password1 and password2):
            errors.append('All fields are required!')
        elif password1 != password2:
            errors.append('Passwords do not match!')
        elif not re.match(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', email):
            errors.append('Invalid email format!')
        elif not is_valid_phone_number(phone_number):
            errors.append('Invalid phone number format! It should be a 10-digit number.')
        elif not is_valid_password(password1):
            errors.append('Password must contain at least 8 characters including one uppercase, one lowercase, one digit, and one special character!')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'sign-up.html')
        else:
            username= username.lower()
            first_name = first_name.title()
            last_name = last_name.title()

            if Account.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists!')
            elif Account.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists!')
            else:
                user = Account.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email,
                                                   phone_number=phone_number, password=password1)
                user = authenticate(email=email, password=password1)
                if user is not None:
                    login(request, user)
                    return redirect("home")

    return render(request, 'sign-up.html')