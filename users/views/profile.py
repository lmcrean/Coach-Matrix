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
        profile_update_form = ProfileUpdateForm(instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user)
        context = {
            'profile_update_form': profile_update_form,
            'password_form': password_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):        
        profile_update_form = ProfileUpdateForm(instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user)

        if 'update_profile' in request.POST:
            profile_update_form = ProfileUpdateForm(request.POST, instance=request.user)
            if profile_update_form.is_valid():
                profile_update_form.save()
                messages.success(request, 'Your profile has been updated.')
                logger.debug("Profile update successful for user: %s", request.user.username)
                return redirect('my_profile')
            else:
                logger.error("Profile update errors: %s", profile_update_form.errors.as_json())
                for field, errors in profile_update_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")

        elif 'change_password' in request.POST:
            password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password has been changed.')
                return redirect('my_profile')
            else:
                logger.error("Password change errors: %s", password_form.errors.as_json())
                for field, errors in password_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")

        # Pass both forms to context, ensuring they're always defined
        context = {
            'profile_update_form': profile_update_form,
            'password_form': password_form,
        }
        return render(request, self.template_name, context)

    