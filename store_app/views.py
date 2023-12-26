# Create your views here.
import re
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import models
#from .forms import LoginForm

def store_home(request):
    return render(request, 'index.html')


def sign_in(request):
    
    if request.user.is_authenticated:
        return redirect("store_home")
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Username does not exist')
            return render(request, 'sign-in.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("store_home")
            #return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, 'Username OR Password is incorrect')

    return render(request, 'sign-in.html')

def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect("store_home")


def is_valid_password(password):
    # Password complexity: At least 8 characters including one uppercase, one lowercase, one digit, and one special character
    return bool(re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password))

def sign_up(request):

    if request.user.is_authenticated:
        return redirect("store_home")
     
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        errors = []

        if not (username and first_name and last_name and email and password1 and password2):
            errors.append('All fields are required!')
        elif password1 != password2:
            errors.append('Passwords do not match!')
        elif not re.match(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', email):
            errors.append('Invalid email format!')
        elif not is_valid_password(password1):
            errors.append('Password must contain at least 8 characters including one uppercase, one lowercase, one digit, and one special character!')
        
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            username= username.lower()
            first_name = first_name.title()
            last_name = last_name.title()

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists!')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists!')
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password1)
                
                # The user object is already saved to the database by create_user
                # No need to call user.save() explicitly in this case
                #user.save()

                user = authenticate(username=username, password=password1)

                if user is not None:
                    login(request, user)
                    return redirect("store_home")

    return render(request, 'sign-up.html')