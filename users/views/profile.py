# users/views/profile.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from ..forms import ProfileUpdateForm, CustomPasswordChangeForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

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
        # Initialize context with empty forms to be populated after determining which form is submitted
        context = {
            'form': ProfileUpdateForm(instance=request.user),
            'password_form': CustomPasswordChangeForm(user=request.user),
        }

        if 'update_profile' in request.POST:
            # If the profile update form is submitted, only process this form
            context['form'] = form = ProfileUpdateForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your profile has been updated.')
            else:
                messages.error(request, 'Please correct the error in the profile form.')
                messages.error(request, form.errors)
                print(form.errors)

        elif 'change_password' in request.POST:
            # If the password change form is submitted, only process this form
            context['password_form'] = password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password has been changed.')
            else:
                messages.error(request, 'Please correct the error in the password form.')
                messages.error(request, password_form.errors)

        # The context now contains either the profile form or the password form, depending on which one was submitted
        return render(request, self.template_name, context)