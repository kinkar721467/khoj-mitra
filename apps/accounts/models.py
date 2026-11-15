"""
accounts/models.py – The User model for Khoj Mitra.

What this file does:
  Defines our custom user with extra fields (roll number, phone, role).
  We extend Django's AbstractUser so we get password hashing and
  login/logout for free, and just ADD what we need.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Our campus user.
    Extends Django's built-in user, so password hashing,
    login/logout and sessions all work automatically.
    """

    # Role choices: a student uses the platform; an admin moderates it.
    ROLE_STUDENT = "student"
    ROLE_ADMIN   = "admin"
    ROLE_CHOICES = [
        (ROLE_STUDENT, "Student"),
        (ROLE_ADMIN,   "Admin"),
    ]

    # --- Extra fields beyond Django's default (username, email, password) ---

    # College email is the primary login identifier.
    # unique=True means two users cannot share the same email.
    college_email = models.EmailField(unique=True)

    # Roll number, e.g. "22CS042"
    roll_number = models.CharField(max_length=20, blank=True)

    # 10-digit mobile number
    phone = models.CharField(max_length=15, blank=True)

    # Role: student by default; manually promoted to admin.
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_STUDENT)

    # An admin can block a misbehaving student.
    is_blocked = models.BooleanField(default=False)

    # When this account was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # Tell Django to use college_email for login instead of username.
    USERNAME_FIELD  = "college_email"
    # username is no longer required when creating a user.
    REQUIRED_FIELDS = ["username"]

    class Meta:
        # The name of the MongoDB collection for this model.
        # Using 'km_users' to avoid conflicts with Atlas sample data 'users' collection.
        db_table = "km_users"

    def __str__(self):
        # Friendly label shown in admin and shell.
        return f"{self.get_full_name()} ({self.college_email})"

    @property
    def is_admin_role(self):
        """True if this user is an admin (not just a Django superuser)."""
        return self.role == self.ROLE_ADMIN
