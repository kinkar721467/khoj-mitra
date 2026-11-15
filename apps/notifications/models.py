"""
notifications/models.py – In-app notification records.

What this file does:
  Stores one document per notification. The context processor reads
  these to show the bell badge count. Views list and mark them read.
"""

from django.db import models
from django.conf import settings


class Notification(models.Model):
    """One in-app notification for one user."""

    TYPE_MATCH       = "match"
    TYPE_CLAIM       = "claim"
    TYPE_MARKETPLACE = "marketplace"
    TYPE_CHOICES = [
        (TYPE_MATCH,       "Match"),
        (TYPE_CLAIM,       "Claim"),
        (TYPE_MARKETPLACE, "Marketplace"),
    ]

    # The user this notification is for.
    user    = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    # The human-readable message, e.g. "92% match found for Black laptop charger".
    message = models.TextField()

    # Category: match / claim / marketplace
    type    = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_MATCH)

    # Optional link to the relevant page (match detail, claim page, listing)
    link    = models.CharField(max_length=255, blank=True)

    # Has the user seen / clicked this notification?
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table  = "notifications"
        ordering  = ["-created_at"]   # newest first

    def __str__(self):
        return f"[{self.type}] {self.message[:60]}"
