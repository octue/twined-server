import os
import sys
from urllib.parse import urlparse
import environ
from octue.runner import LOG_FORMAT


# DIRECTORIES AND ENVIRONMENT

# Set the root directories
#
#   REPO_DIR (twined-server/)                Top level working directory at runtime.
#   ROOT_DIR (twined-server/server/)         Root of the server code. Used by third party apps.
#   APPS_DIR (twined-server/server/app)      The django application configuration modules
#   BASE_DIR (twined-server/server/settings) The django settings directory
#   REACT_DIR (twined-server/src/)           The frontend soruce code directory
REPO_DIR = environ.Path(__file__).__sub__(3)  # (twined-server/server/settings/base.py - 3 = twined-server/)
ROOT_DIR = REPO_DIR.path("server").__str__()
APPS_DIR = REPO_DIR.path("server").path("app").__str__()
BASE_DIR = REPO_DIR.path("server").path("settings").__str__()
REACT_BUILD_DIR = REPO_DIR.path("build").__str__()

# Add the ROOT_DIR directory to the system path so django can find the apps without renaming them to e.g. server.reel
# (from https://stackoverflow.com/questions/3948356/how-to-keep-all-my-django-applications-in-specific-folder)
sys.path.insert(0, ROOT_DIR.__str__())

# Load operating system environment variables and then prepare to use them
env = environ.Env()
READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # Operating System Environment variables have precedence over variables defined in the .env file,
    # that is to say variables from the .env file will only be used if not defined as environment variables
    env_file = str(REPO_DIR.path(".env"))
    print("Loading environment from file: {}\n".format(env_file))
    env.read_env(env_file)


# APP CONFIGURATION

ALLOWED_HOSTS = [
    "localhost",
    ".localhost",
    "0.0.0.0",
    "127.0.0.1",
    "octue.dev",
    ".octue.dev",
    "octue.com",
    ".octue.com",
]

DEBUG = env.bool("DJANGO_DEBUG", False)

INSTALLED_APPS = [
    "channels",
    "django.contrib.staticfiles",
    "reel.apps.ReelAppConfig",
]


# MIDDLEWARE CONFIGURATION

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# TODO filter properly
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True


# CACHING CONFIGURATION


# INTERNATIONALISATION

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# Not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = "UTC"
LANGUAGE_CODE = "en-us"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# TEMPLATE CONFIGURATION

# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(APPS_DIR, "templates")],
        # "DIRS": [os.path.join(APPS_DIR, "templates"), REACT_BUILD_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            "debug": DEBUG,
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "app.context_processors.app_rendering_ctx",
            ],
        },
    },
]


# STATIC FILES

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = str(REPO_DIR.path("static_files"))

# Add the directories where static assets are built by node, with each of their namespaces
# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
    # ("js", str(REPO_DIR.path("build").path("static").path("js"))),
    # ("css", str(REPO_DIR.path("build").path("static").path("css"))),
    # ("media", str(REPO_DIR.path("build").path("static").path("media"))),
]


# MEDIA FILES
MEDIA_ROOT = str(REPO_DIR.path("media_files"))
MEDIA_URL = "/media/"


# WSGI/URL CONFIGURATION

ROOT_URLCONF = "app.urls"
WSGI_APPLICATION = "app.wsgi.application"
ASGI_APPLICATION = "app.asgi.application"


# AUTH SETTINGS, PASSWORD STORAGE AND VALIDATION

# Hashing algorithm
# See https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]


# TODO CUSTOM AUTHENTICATION BACKEND
AUTHENTICATION_BACKENDS = ()


# DJANGO UTILITIES

AUTOSLUG_SLUGIFY_FUNCTION = "slugify.slugify"


# DRF_SIGNED_AUTH
# When signing tokens to access files, use 1 day.
SIGNED_URL_TTL = 60 * 60 * 24


# REDIS


def parse_redis_url(url):
    """ Parses a redis url into component parts, stripping password from the host

    Long keys in the url result in parsing errors, since labels within a hostname cannot exceed 64 characters under
    idna rules... See https://stackoverflow.com/questions/62777377/long-url-including-a-key-causes-unicode-idna-codec-decoding-error-whilst-using/62777378#62777378

    In that event, we remove the key/password so that it can be passed separately to the RedisChannelLayer and therefore
    not violate length rules.

    Also, Heroku REDIS_URL does not include the DB number, so we allow for a default value of '0'
    """
    parsed = urlparse(url)
    parts = parsed.netloc.split(":")
    host = ":".join(parts[0:-1])
    port = parts[-1]
    path = parsed.path.split("/")[1:]
    db = int(path[0]) if len(path) >= 1 else 0

    user, password = (None, None)
    if "@" in host:
        creds, host = host.split("@")
        user, password = creds.split(":")
        host = f"{user}@{host}"

    return host, port, user, password, db


REDIS_URL = env("REDIS_URL", default="redis://localhost:6379")
REDIS_HOST, REDIS_PORT, REDIS_USER, REDIS_PASSWORD, REDIS_DB = parse_redis_url(REDIS_URL)
REDIS_LOCATION = f"{REDIS_URL}/{REDIS_DB}"


# DJANGO CHANNELS

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [{"address": f"redis://{REDIS_HOST}:{REDIS_PORT}", "db": REDIS_DB, "password": REDIS_PASSWORD}],
        },
    },
}


# TESTING
TESTING = env.bool("TESTING", default=False)


# LOGGING

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {"level": "WARNING", "handlers": ["console"]},
    "formatters": {"verbose": {"format": LOG_FORMAT}},
    "handlers": {"console": {"level": "INFO", "class": "logging.StreamHandler", "formatter": "verbose"}},
    "loggers": {
        "app": {"level": "INFO", "handlers": ["console"], "propagate": False},
        "reel": {"level": "INFO", "handlers": ["console"], "propagate": False},
    },
}

# INTEGRATIONS - GOOGLE

# We want GA code to be rendered in production if given
GOOGLE_ANALYTICS_ID = env.str("GOOGLE_ANALYTICS_ID", None)

# Test keys as per https://developers.google.com/recaptcha/docs/faq
#   "With the following test keys, you will always get No CAPTCHA and all verification requests will pass."
RECAPTCHA_PUBLIC_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
RECAPTCHA_PRIVATE_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"
NOCAPTCHA = True
SILENCED_SYSTEM_CHECKS = ["captcha.recaptcha_test_key_error"]
