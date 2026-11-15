"""dashboard/views.py – Stub view for Phase 1."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def admin_dashboard(request):
    """Screen 11 – Admin dashboard (built in Phase 7)."""
    return render(request, "lostfound/coming_soon.html",
                  {"page": "Admin dashboard"})
