# users/forms.py

# this is the form that will be used to update the user's profile
# it includes:
# 1. custom form fields for log in and sign up
# 2. a form for updating the user's profile
# 3. a form for changing the user's password

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.exceptions import ValidationError
import re
from better_profanity import profanity

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)

class CustomSignupForm(UserCreationForm):
    """
    Custom form for signing up a new user.

    1. The username field is required and must be between 3 to 20 characters long. It can only contain letters and numbers.
    2. The password field is required and must be between 8 to 30 characters long. It must contain at least one number and one special character.
    3. The confirm password field is required and must match the password field.
    """

    username = forms.CharField(max_length=20, min_length=3, required=True, help_text='Required. 3 to 20 characters. Letters and numbers only.')
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput, help_text='Required. 8 to 30 characters. Must include 1 number and 1 special character.')
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput, help_text='Enter the same password as before, for verification.')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def clean_username(self):
        """
        1. get the username from the cleaned data
        2. check if the username only contains letters and numbers
        3. check if the username already exists
        4. check if username contains profanity
        """
        username = self.cleaned_data['username'].strip()
        if not re.match(r'^\w+$', username):
            raise ValidationError("Username can only contain letters and numbers.")
        if User.objects.filter(username=username).exists():
            raise ValidationError("A user with that username already exists.")
        if profanity.contains_profanity(username):
            raise ValidationError("Please remove any profanity from the username.")
        return username

    def clean_password2(self):
        """
        1. get the password1 and password2 from the cleaned data
        2. check if the passwords match
        3. check if the password contains at least one number
        4. check if the password contains at least one special character
        5. check if the password is between 8 to 30 characters long
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match.")

        if not re.search(r'\d', password1):
            raise ValidationError("The password must contain at least one number.")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
            raise ValidationError("The password must contain at least one special character.")
        
        if len(password1) < 8 or len(password1) > 30:
            raise ValidationError("Password must be between 8 to 30 characters long.")
        
        return password2


class ProfileUpdateForm(forms.ModelForm):
    """
    Custom form for updating the user's profile.

    1. The username field is required and must be between 3 to 20 characters long. It can only contain letters and numbers.
    2. The first name and last name fields are optional, they must be between 2 to 100 characters long.
    3. original username validation criteria applies when updating the username.
    4. user cannot place profanity in first name and last name fields.
    """
    username = forms.CharField(max_length=20, min_length=3, required=True, help_text='Required. 3 to 20 characters. Letters and numbers only.')
    first_name = forms.CharField(max_length=100, min_length=2, required=False, help_text='Optional. 2 to 100 characters.')
    last_name = forms.CharField(max_length=100, min_length=2, required=False, help_text='Optional. 2 to 100 characters.')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Update Profile'))

    def clean_username(self):
        """
        1. get the username from the cleaned data
        2. check if the username only contains letters and numbers
        3. check if the username already exists, excluding the current user
        4. check if username contains profanity
        """
        username = self.cleaned_data['username'].strip()
        if not re.match(r'^\w+$', username):
            raise ValidationError("Username can only contain letters and numbers.")
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError("A user with that username already exists.")
        if profanity.contains_profanity(username):
            raise ValidationError("Please remove any profanity from the username.")
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', '').strip()
        if first_name and (len(first_name) < 2 or len(first_name) > 100):
            raise ValidationError("First name must be between 2 to 100 characters.")
        if profanity.contains_profanity(first_name):
            raise ValidationError("Please remove any profanity from the first name.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name', '').strip()
        if last_name and (len(last_name) < 2 or len(last_name) > 100):
            raise ValidationError("Last name must be between 2 to 100 characters.")
        if profanity.contains_profanity(last_name):
            raise ValidationError("Please remove any profanity from the last name.")
        return last_name

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Change Password'))