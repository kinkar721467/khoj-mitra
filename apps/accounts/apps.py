from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django_mongodb_backend.fields.ObjectIdAutoField"
    name = "apps.accounts"
    label = "accounts"

    def ready(self):
        """
        Called when Django finishes loading all apps.
        We disconnect the broken post_migrate signal here — AFTER the auth
        app has had a chance to register it in its own ready() — so our
        disconnect is the last word.
        """
        from django.db.models.signals import post_migrate
        from django.contrib.auth.management import create_permissions
        post_migrate.disconnect(create_permissions)
