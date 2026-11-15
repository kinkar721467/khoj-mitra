"""
accounts/admin.py – Registers User in Django's built-in admin panel.

What this file does:
  Makes the User model visible in /admin/ with useful columns and filters.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Columns shown in the list view
    list_display  = ("college_email", "get_full_name", "roll_number", "role", "is_blocked", "created_at")
    list_filter   = ("role", "is_blocked", "is_active")
    search_fields = ("college_email", "first_name", "last_name", "roll_number")
    ordering      = ("-created_at",)

    # Add our custom fields to the edit form in admin
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Campus info", {
            "fields": ("college_email", "roll_number", "phone", "role", "is_blocked"),
        }),
    )
