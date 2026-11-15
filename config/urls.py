"""
urls.py – The main URL router for Khoj Mitra.

What this file does:
  Maps top-level URL paths to each app's own urls.py file.
  Also serves media (uploaded photos) during development.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django's built-in admin panel (useful for quick data inspection)
    path("admin/", admin.site.urls),

    # Accounts: register, login, logout, profile
    path("accounts/", include("apps.accounts.urls")),

    # Lost and found: report, list, detail
    path("lostfound/", include("apps.lostfound.urls")),

    # Marketplace: buy and sell listings
    path("marketplace/", include("apps.marketplace.urls")),

    # Notifications: list and mark-as-read
    path("notifications/", include("apps.notifications.urls")),

    # Admin dashboard (our custom one, not Django admin)
    path("dashboard/", include("apps.dashboard.urls")),

    # Home page lives in accounts app (it's the landing page)
    path("", include("apps.accounts.urls")),
]

# In development, Django serves uploaded media files directly.
# In production you would use a web server (nginx) for this.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
