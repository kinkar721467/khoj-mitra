"""
accounts/urls.py – URL patterns for the accounts app.

What this file does:
  Maps URL paths like /accounts/register/ to the right view function.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Home page (Screen 1)
    path("",                views.home_view,     name="home"),

    # Auth pages
    path("accounts/register/", views.register_view, name="register"),
    path("accounts/login/",    views.login_view,    name="login"),
    path("accounts/logout/",   views.logout_view,   name="logout"),
    path("accounts/profile/",  views.profile_view,  name="profile"),
]
