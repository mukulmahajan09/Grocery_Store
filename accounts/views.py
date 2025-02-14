# Create your views here.
import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .models import Account, UserProfile
from django.contrib import messages
from django.db import models
from django.conf import settings
from .forms import UserForm, UserProfileForm

# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required


def store_home(request):
    return render(request, 'base.html')


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
            return render(request, 'accounts/sign-in.html')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
            #return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, 'Username OR Password is incorrect')

    return render(request, 'accounts/sign-in.html')


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
            return render(request, 'accounts/sign-up.html')
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
                
                # USER ACTIVATION
                current_site = get_current_site(request)
                mail_subject = 'Please activate your account'
                message = render_to_string('accounts/account_verification_email.html', {
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                to_email = email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()
                return redirect('/users_accounts/sign-in/?command=verification&email='+email)

    return render(request, 'accounts/sign-up.html')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated. Please Sign In')
        return redirect('sign-in')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('sign-up')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'We have sent you an email to reset your password!')
            return redirect('sign-in')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgot_password')
        
    return render(request, 'accounts/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('sign-in')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if not is_valid_password(password):
                messages.error('Password must contain at least 8 characters including one uppercase, one lowercase, one digit, and one special character!')
            else:
                uid = request.session.get('uid')
                user = Account.objects.get(pk=uid)
                user.set_password(password)
                user.save()
    
                # Send password reset confirmation email
                mail_subject = 'Password Reset Confirmation'
                message = 'Your password has been reset successfully. If you did not perform this action, please contact us immediately.'
                to_email = user.email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()
    
                messages.success(request, 'Password reset successfully')
                return redirect('sign-in')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('reset_password')
    else:
        return render(request, 'accounts/reset_password.html')


#@login_required(login_url='login')
#def change_password(request):
#    if request.method == 'POST':
#        current_password = request.POST['current_password']
#        new_password = request.POST['new_password']
#        confirm_password = request.POST['confirm_password']
#
#        user = Account.objects.get(username__exact=request.user.username)
#
#        if new_password == confirm_password:
#            success = user.check_password(current_password)
#            if success:
#                user.set_password(new_password)
#                user.save()
#                # auth.logout(request)
#                messages.success(request, 'Password updated successfully.')
#                return redirect('change_password')
#            else:
#                messages.error(request, 'Please enter valid current password')
#                return redirect('change_password')
#        else:
#            messages.error(request, 'Password does not match!')
#            return redirect('change_password')
#    return render(request, 'accounts/change_password.html')


@login_required(login_url = 'sign-in')
def user_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user.id)

    context = {
        'userprofile': userprofile
    }

    return render(request, 'store/user_profile.html', context)


@login_required(login_url = 'sign-in')
def edit_user_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        user_profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        # add remaining functionality

        if user_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            user_profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        user_profile_form = UserProfileForm(instance=user_profile)

    context = {
        'user_form': 'user_form',
        'user_profile': 'user_profile',
        'user_profile_form': 'user_profile_form',
    }

    return render(request, 'accounts/edit_profile.html', context)