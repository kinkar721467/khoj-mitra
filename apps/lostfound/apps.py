from django.apps import AppConfig
class LostfoundConfig(AppConfig):
    default_auto_field = "django_mongodb_backend.fields.ObjectIdAutoField"
    name = "apps.lostfound"
    label = "lostfound"
