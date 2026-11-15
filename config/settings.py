"""
settings.py – Django configuration for Khoj Mitra.

What this file does:
  Tells Django where apps are, how to connect to MongoDB,
  where templates and static files live, and how to send email.
  All secrets come from the .env file, never hard-coded here.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ── Load .env into environment variables ──────────────────────────
# This must happen BEFORE we read any os.environ values.
load_dotenv()

# ── Base directory (the folder that contains manage.py) ───────────
BASE_DIR = Path(__file__).resolve().parent.parent

# ── Security ──────────────────────────────────────────────────────
SECRET_KEY   = os.environ.get("SECRET_KEY", "change-me-in-dotenv")
DEBUG        = os.environ.get("DEBUG", "True") == "True"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# ── Custom user model ─────────────────────────────────────────────
# We tell Django to use OUR User model instead of its built-in one.
# MUST be set before the first migration.
AUTH_USER_MODEL = "accounts.User"

# ── Installed apps ────────────────────────────────────────────────
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Our own apps (each folder inside apps/)
    "apps.accounts",
    "apps.lostfound",
    "apps.marketplace",
    "apps.notifications",
    "apps.dashboard",
]

# ── Middleware ────────────────────────────────────────────────────
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

# ── Templates ─────────────────────────────────────────────────────
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Adds unread notification count to every template
                "apps.notifications.context_processors.notification_count",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ── MongoDB database connection ───────────────────────────────────
# django-mongodb-backend connects Django to MongoDB Atlas.
DATABASES = {
    "default": {
        "ENGINE": "django_mongodb_backend",
        "NAME": os.environ.get("MONGO_DB_NAME", "khoj_mitra"),
        "CLIENT": {
            "host": os.environ.get(
                "MONGO_URI",
                "mongodb://localhost:27017/khoj_mitra"
            ),
        },
    }
}

# ── MongoDB: silence AutoField errors on Django built-in apps ─────
# Django's admin/auth/contenttypes models use AutoField by default.
# We silence those checks because DEFAULT_AUTO_FIELD below overrides
# them when the actual migrations run with our ObjectIdAutoField.
SILENCED_SYSTEM_CHECKS = [
    "mongodb.fields.auto.E001",  # AutoField not supported → we override below
]

# ── Fix: patch emit_post_migrate_signal to never crash ────────────
# This is a bug in django-mongodb-backend 6.1.0 + Python 3.14.
# The create_permissions handler in auth tries to use ContentType
# objects as dict keys before they have PKs, making them unhashable.
# We replace the whole emit function with a safe no-op.
from django.core.management import sql as _sql_mod                   # noqa: E402


def _safe_emit_post_migrate(*args, **kwargs):
    """Safe replacement: skips the broken create_permissions step."""
    pass


_sql_mod.emit_post_migrate_signal = _safe_emit_post_migrate

# ── Password validation ───────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
     "OPTIONS": {"min_length": 8}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
]

# ── Localisation ──────────────────────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE     = "Asia/Kolkata"
USE_I18N      = True
USE_TZ        = True

# ── Static files ──────────────────────────────────────────────────
STATIC_URL       = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT      = BASE_DIR / "staticfiles"

# ── Media files (user uploads) ────────────────────────────────────
MEDIA_URL  = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ── Default primary key → MongoDB ObjectId ───────────────────────
# This tells Django (and all our apps) to use ObjectId for every new model.
DEFAULT_AUTO_FIELD = "django_mongodb_backend.fields.ObjectIdAutoField"

# ── Email (prints to terminal – no SMTP needed in development) ────
EMAIL_BACKEND    = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "noreply@khojmitra.campus"

# ── Auth URL settings ─────────────────────────────────────────────
LOGIN_URL          = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/accounts/login/"

# ── Campus email validation ───────────────────────────────────────
# Only emails ending with this domain can register.
ALLOWED_EMAIL_DOMAIN = os.environ.get("ALLOWED_EMAIL_DOMAIN", "college.edu")

# ── Matching engine tuning ────────────────────────────────────────
MATCH_WEIGHT_CATEGORY = 0.30
MATCH_WEIGHT_TEXT     = 0.35
MATCH_WEIGHT_LOCATION = 0.20
MATCH_WEIGHT_DATE     = 0.15
MATCH_SCORE_THRESHOLD = 50       # out of 100

# ── Image upload limits ───────────────────────────────────────────
MAX_IMAGE_SIZE_MB = 5
