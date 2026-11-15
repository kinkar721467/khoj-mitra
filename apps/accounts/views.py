"""
accounts/views.py – Register, login, logout and profile pages.

What this file does:
  Thin views that handle HTTP requests, call forms, and render templates.
  Business logic (email check) lives in forms.py, not here.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime

from .forms import RegisterForm, LoginForm
from .models import User


def register_view(request):
    """Screen 6 – Create a new account."""
    # If the user is already logged in, send them to the home page.
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in immediately after registration.
            login(request, user)
            messages.success(request, f"Welcome to Khoj Mitra, {user.first_name}!")
            return redirect("home")
    else:
        # GET request: show an empty form.
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    """Screen 3 – Sign in with college email and password."""
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            # Block check: blocked users cannot log in.
            if user.is_blocked:
                messages.error(request, "Your account has been blocked. Contact admin.")
                return redirect("login")

            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name}!")
            # Redirect to the page the user originally tried to visit,
            # or the home page if they came directly to login.
            next_url = request.GET.get("next", "/")
            return redirect(next_url)
    else:
        form = LoginForm(request)

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    """Log out and redirect to login page."""
    logout(request)
    messages.info(request, "You have been signed out.")
    return redirect("login")


@login_required
def profile_view(request):
    """Profile page: shows the user's own reports, claims and listings."""
    user = request.user
    return render(request, "accounts/profile.html", {"profile_user": user})


@login_required
def home_view(request):
    """Screen 1 – Home page with greeting and recent activity."""
    hour = datetime.now().hour
    if hour < 12:
        greeting = "morning"
    elif hour < 17:
        greeting = "afternoon"
    else:
        greeting = "evening"

    context = {
        "greeting":     greeting,
        "user_reports": [],   # filled in Phase 2
        "recent_found": [],   # filled in Phase 2
    }
    return render(request, "accounts/home.html", context)
