"""dashboard/urls.py – URL patterns (Phase 7 will expand these)."""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.admin_dashboard, name="admin_dashboard"),
]
