from pathlib import Path
import os
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("DJANGO_SECRET_KEY", default="change-me-in-production")

# Use DJANGO_DEBUG to avoid conflicts with Python's DEBUG variable
try:
    DEBUG = config("DJANGO_DEBUG", default="True", cast=lambda v: str(v).lower() in ("true", "1", "yes"))
except:
    DEBUG = True

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1,*", cast=lambda v: [s.strip() for s in v.split(",") if s.strip()])

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "users",
    "licenses",
    "vehicles",
    "partnerships",
    "payments",
    "applications",
    "documents",
    "systemsettings",
]

# Use custom user model from `users` app
AUTH_USER_MODEL = "users.CustomUser"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend_project.wsgi.application"

# Database configuration using environment variables
# Works with both local .env file and Render environment variables
DATABASES = {
    "default": {
        "ENGINE": config("DB_ENGINE", default="django.db.backends.postgresql"),
        "NAME": config("DB_NAME", default="clms"),
        "USER": config("DB_USER", default="postgres"),
        "PASSWORD": config("DB_PASSWORD", default="postgress"),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="5432"),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

# CORS Configuration for frontend deployment on Vercel
CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    default="http://localhost:3000,http://127.0.0.1:3000",
    cast=lambda v: [s.strip() for s in v.split(",") if s.strip()]
)

# Allow all origins in development if needed (not recommended for production)
CORS_ALLOW_ALL_ORIGINS = config("CORS_ALLOW_ALL_ORIGINS", default=False, cast=bool)

# Additional CORS settings
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]
