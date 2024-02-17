# users/views.py
import logging
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.urls import reverse
from .forms import CustomLoginForm


def home(request):
    return render(request, "index.html")

def questions_view(request):
    print('Redirecting to questions page')
    return redirect(reverse('questions'))

def logout_view(request):
    logout(request)
    return redirect(reverse('home'))



logger = logging.getLogger(__name__)

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
    else:
        form = CustomLoginForm()

    return render(request, 'login.html', {'form': form})
