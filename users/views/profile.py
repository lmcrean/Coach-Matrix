# users/views/profile.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from ..forms import ProfileUpdateForm, CustomPasswordChangeForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

import logging

logger = logging.getLogger(__name__)

class ProfileView(LoginRequiredMixin, View):
    template_name = 'my_profile.html'

    def get(self, request, *args, **kwargs):
        form = ProfileUpdateForm(instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user)
        context = {
            'form': form,
            'password_form': password_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        if 'update_profile' in request.POST:
            form = ProfileUpdateForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your profile has been updated.')
                print(f"Updated username: {updated_user.username}")
                return redirect('my_profile')
            else:
                logger.error(f"Profile update errors: {form.errors}")
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")

        elif 'change_password' in request.POST:
            password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password has been changed.')
                return redirect('my_profile')  # Redirect to refresh the page and clear the form
            else:
                for field, errors in password_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")

        else:
            form = ProfileUpdateForm(instance=request.user)
            password_form = CustomPasswordChangeForm(user=request.user)

        context = {
            'form': form,
            'password_form': password_form,
        }

        if form.is_valid():
            form.save()
            updated_user = User.objects.get(id=request.user.id)  # Fetch the user again from the database
            logger.debug(f"Updated username: {updated_user.username}")  # Log the updated username
            messages.success(request, 'Your profile has been updated.')
            return redirect('my_profile')

        return render(request, self.template_name, context)

    