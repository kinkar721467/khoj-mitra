"""marketplace/views.py – Stub view for Phase 1."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def marketplace_list(request):
    """Screen 5 – Marketplace (built in Phase 6)."""
    return render(request, "lostfound/coming_soon.html",
                  {"page": "Campus marketplace"})
