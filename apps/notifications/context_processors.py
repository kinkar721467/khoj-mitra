"""
notifications/context_processors.py – Adds the unread count to every page.

What this file does:
  Django calls this function on every request and merges its return value
  into the template context. This is how the bell badge in the top bar
  always shows the correct unread count without each view calculating it.
"""

from django.db.models import Q


def notification_count(request):
    """Return the number of unread notifications for the logged-in user."""
    if request.user.is_authenticated:
        # Import here (not at top) to avoid circular imports during startup.
        from apps.notifications.models import Notification
        count = Notification.objects.filter(
            user=request.user,
            is_read=False,
        ).count()
        return {"unread_notification_count": count}

    # For anonymous users, the count is zero.
    return {"unread_notification_count": 0}
