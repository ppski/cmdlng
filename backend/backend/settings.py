import os
from pathlib import Path
from decouple import config


# ------------------------------------------------------------ #
# Lang-related
# ------------------------------------------------------------ #
LEXICALA_API_KEY = config("LEXICALA_API_KEY")
LANG_SOURCE = "fr_fr"
LANG_TARGET = "en_us"

# ------------------------------------------------------------ #
# LLM-related
# ------------------------------------------------------------ #
LLM_OPTIONS = ["chatgpt", "llama"]

# Define the below in env
DEFAULT_LLM = config("DEFAULT_LLM")
OPENAI_API_KEY = config("OPENAI_API_KEY")
OPENAI_MODEL = config("OPENAI_MODEL")
LOCAL_LLAMA_MODEL = config("LOCAL_LLAMA_MODEL")
DEFAULT_LOCAL_LLM = config("DEFAULT_LOCAL_LLM")

# ------------------------------------------------------------ #
# Django settings
# ------------------------------------------------------------ #
ALLOWED_HOSTS = []
BASE_DIR = Path(__file__).resolve().parent.parent
CORS_ORIGIN_ALLOW_ALL = True  # Only for local use
DEBUG = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DJANGO_SETTINGS_MODULE = "backend.settings"
SECRET_KEY = "*"
STATIC_URL = "static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# Internationalization
DATE_INPUT_FORMATS = ["%Y-%m-%dT%H:%M:%S"]
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Paris"
USE_I18N = True
USE_TZ = True


INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "rest_framework",
    "words",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "backend.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
