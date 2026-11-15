"""
accounts/forms.py – Registration and login forms.

What this file does:
  Defines the HTML form fields and their validation rules.
  The college email domain check lives here.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.conf import settings
from .models import User


class RegisterForm(UserCreationForm):
    """
    Registration form shown on Screen 6.
    Validates that the email ends with the allowed college domain.
    """

    full_name = forms.CharField(
        max_length=100,
        label="Full name",
        widget=forms.TextInput(attrs={
            "placeholder": "Your name",
            "class": "form-control km-input",
        }),
    )

    college_email = forms.EmailField(
        label="College email",
        help_text="Only college email addresses are accepted.",
        widget=forms.EmailInput(attrs={
            "placeholder": "name@college.edu",
            "class": "form-control km-input",
        }),
    )

    roll_number = forms.CharField(
        max_length=20,
        label="Roll number",
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "e.g. 22CS042",
            "class": "form-control km-input",
        }),
    )

    phone = forms.CharField(
        max_length=15,
        label="Phone",
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "10-digit number",
            "class": "form-control km-input",
        }),
    )

    # Override the two password fields to match our style.
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "At least 8 characters",
            "class": "form-control km-input",
        }),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Repeat password",
            "class": "form-control km-input",
        }),
    )

    class Meta:
        model  = User
        fields = ["full_name", "college_email", "roll_number", "phone",
                  "password1", "password2"]

    def clean_college_email(self):
        """
        Custom validation: reject any email that doesn't end with
        the allowed domain set in settings.py (read from .env).
        """
        email  = self.cleaned_data["college_email"].strip().lower()
        domain = settings.ALLOWED_EMAIL_DOMAIN.lower()

        if not email.endswith(f"@{domain}"):
            raise forms.ValidationError(
                f"Only @{domain} email addresses are accepted on this platform."
            )
        return email

    def save(self, commit=True):
        """
        Save the new user.
        We split full_name into first_name + last_name and set username.
        """
        user = super().save(commit=False)

        # Split name into first / last (last part is last name, rest is first)
        parts = self.cleaned_data["full_name"].strip().split()
        user.first_name = " ".join(parts[:-1]) if len(parts) > 1 else parts[0]
        user.last_name  = parts[-1] if len(parts) > 1 else ""

        # Use email as the username as well (keeps things simple)
        user.username      = self.cleaned_data["college_email"]
        user.college_email = self.cleaned_data["college_email"]
        user.roll_number   = self.cleaned_data.get("roll_number", "")
        user.phone         = self.cleaned_data.get("phone", "")

        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """
    Login form shown on Screen 3.
    Uses Django's built-in AuthenticationForm and just re-styles the fields.
    """

    username = forms.EmailField(
        label="College email",
        widget=forms.EmailInput(attrs={
            "placeholder": "name@college.edu",
            "class": "form-control km-input",
            "autofocus": True,
        }),
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter your password",
            "class": "form-control km-input",
        }),
    )
