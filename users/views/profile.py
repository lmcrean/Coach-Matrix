# users/views/profile.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from ..forms import ProfileUpdateForm, CustomPasswordChangeForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


# import logging

# logger = logging.getLogger(__name__)

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
        try:
            password_form = CustomPasswordChangeForm(data=request.POST, user=request.user) # this section was tested as working, or at least it was tested as not throwing an error
        except Exception as e:
            messages.error(request, "An error occurred during form processing.")
            password_form = CustomPasswordChangeForm(user=request.user)  # Re-initialize form for context

        if request.POST.get('form_type') == 'update_profile': # this section was tested as working
            profile_update_form = ProfileUpdateForm(request.POST, instance=request.user)
            
            if profile_update_form.is_valid(): # this section was tested as working
                profile_update_form.save()
                messages.success(request, 'Your profile has been updated.')
                return redirect('my_profile')
            else:
                for field, errors in profile_update_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")

        elif request.POST.get('form_type') == 'change_password': 
            if password_form.is_valid():
                user = password_form.save()  
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password has been changed.') 
                return redirect('my_profile') # this line was tested as working, or at least it was tested as not throwing an error
            else:
                for field, errors in password_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")

        # Pass both forms to context, ensuring they're always defined
        context = {
            'profile_update_form': profile_update_form,
            'password_form': password_form,
        }
        return render(request, self.template_name, context)

    