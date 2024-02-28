# users/views/authentication.py
import logging
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib import messages
from django.urls import reverse
from ..forms import CustomLoginForm, CustomSignupForm, CustomPasswordChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_backends
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required


logger = logging.getLogger(__name__)

def home(request):
    if request.user.is_authenticated:
        return redirect(reverse('questions'))
    return render(request, "index.html")

def questions_view(request):
    return render(request, "questions.html")

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect(reverse('home'))

def custom_login_view(request):
    if request.method == 'POST':
        logger.debug('Attempting to authenticate a user.')
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                logger.info(f'User {username} authenticated successfully.')
                login(request, user)
                return redirect(reverse('questions')) 
            else:
                logger.warning(f'Failed login attempt for user {username}.')
                messages.error(request, 'Username or password is incorrect.')
        else:
            logger.error('LoginForm is invalid: %s', form.errors)
            messages.error(request, 'Please correct the error below.')
            messages.error(request, form.errors)
    else:
        # Redirect to home if the user is already logged in
        if request.user.is_authenticated:
            return redirect(reverse('questions'))
        form = CustomLoginForm()

    # Directly render the index page which contains the login form
    return render(request, 'index.html', {'form': form})

def custom_signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Specify the backend to use
            backend = get_backends()[0]
            user.backend = f'{backend.__module__}.{backend.__class__.__name__}'
            login(request, user)
            return redirect(reverse('questions'))  # Redirect to 'questions' after sign-up
        else:
            # If the form is invalid, render 'index.html' with form errors
            messages.error(request, 'Please correct the error below.')
            messages.error(request, form.errors)
            return render(request, 'index.html', {'signup_form': form})
    else:
        form = CustomSignupForm()
        return render(request, 'index.html', {'signup_form': form})
