"""
notifications/views.py – List notifications and mark them as read.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification


@login_required
def notification_list(request):
    """Screen 8 – All notifications for the logged-in user."""
    filter_type = request.GET.get("type", "all")

    qs = Notification.objects.filter(user=request.user)

    if filter_type == "unread":
        qs = qs.filter(is_read=False)
    elif filter_type in ("match", "claim", "marketplace"):
        qs = qs.filter(type=filter_type)

    filter_choices = [
        ("All",         "all"),
        ("Unread",      "unread"),
        ("Matches",     "match"),
        ("Claims",      "claim"),
        ("Marketplace", "marketplace"),
    ]
    return render(request, "notifications/list.html", {
        "notifications":  qs,
        "filter_type":    filter_type,
        "filter_choices": filter_choices,
    })


@login_required
def mark_read(request, pk):
    """Mark one notification as read, then redirect back."""
    notif = get_object_or_404(Notification, pk=pk, user=request.user)
    notif.is_read = True
    notif.save()
    if notif.link:
        return redirect(notif.link)
    return redirect("notification_list")


@login_required
def mark_all_read(request):
    """Mark all notifications as read."""
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect("notification_list")
