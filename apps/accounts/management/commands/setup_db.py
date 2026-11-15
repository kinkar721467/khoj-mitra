"""
setup_db.py – Custom management command to safely migrate MongoDB.

What this file does:
  Runs Django migrations but disconnects the broken post_migrate signal
  that crashes on django-mongodb-backend + Python 3.14.
  Run with: python manage.py setup_db
"""

from django.core.management.base import BaseCommand
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.contrib.auth.management import create_permissions
from django.db.models.signals import post_migrate


class Command(BaseCommand):
    help = "Run all migrations safely for MongoDB (bypasses post_migrate bug)"

    def handle(self, *args, **options):
        self.stdout.write("Disconnecting broken post_migrate signal...")

        # Temporarily disconnect the signal that crashes on MongoDB
        post_migrate.disconnect(create_permissions)

        try:
            self.stdout.write("Running migrations...")
            executor = MigrationExecutor(connection)
            targets = executor.loader.graph.leaf_nodes()
            plan = executor.migration_plan(targets)

            if not plan:
                self.stdout.write(self.style.SUCCESS("No migrations to apply."))
            else:
                self.stdout.write(f"Applying {len(plan)} migration(s)...")
                executor.migrate(targets)
                self.stdout.write(self.style.SUCCESS("All migrations applied!"))

            # Manually create permissions now (safely)
            self.stdout.write("Creating permissions...")
            self._create_permissions_safely()
            self.stdout.write(self.style.SUCCESS("Done! Database is ready."))

        finally:
            # Always reconnect the signal
            post_migrate.connect(create_permissions)

    def _create_permissions_safely(self):
        """Create auth permissions without crashing on unhashable ContentTypes."""
        from django.apps import apps
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType

        for app_config in apps.get_app_configs():
            app_models = list(app_config.get_models())
            for model in app_models:
                try:
                    ct, _ = ContentType.objects.get_or_create(
                        app_label=model._meta.app_label,
                        model=model._meta.model_name,
                    )
                    # Create the 4 default permissions for this model
                    for codename, name in [
                        (f"add_{model._meta.model_name}",    f"Can add {model._meta.verbose_name}"),
                        (f"change_{model._meta.model_name}", f"Can change {model._meta.verbose_name}"),
                        (f"delete_{model._meta.model_name}", f"Can delete {model._meta.verbose_name}"),
                        (f"view_{model._meta.model_name}",   f"Can view {model._meta.verbose_name}"),
                    ]:
                        Permission.objects.get_or_create(
                            codename=codename,
                            content_type=ct,
                            defaults={"name": name},
                        )
                except Exception as e:
                    # Skip if anything fails – permissions are non-critical for dev
                    self.stdout.write(f"  Skipped {model}: {e}")
