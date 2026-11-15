"""
lostfound/views.py – Stub views for Phase 1.
Phase 2 will replace these with real implementations.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def report_item(request):
    """Screen 2 – Report a lost or found item (built in Phase 2)."""
    return render(request, "lostfound/coming_soon.html",
                  {"page": "Report an item"})


@login_required
def found_list(request):
    """Screen 7 – Browse found items (built in Phase 2)."""
    return render(request, "lostfound/coming_soon.html",
                  {"page": "Found items"})


@login_required
def found_detail(request, pk):
    """Found item detail / claim page (built in Phase 2)."""
    return render(request, "lostfound/coming_soon.html",
                  {"page": "Item detail"})


@login_required
def my_matches(request):
    """Screen 4 – Match list (built in Phase 3)."""
    return render(request, "lostfound/coming_soon.html",
                  {"page": "Matches"})
