from .base import *  # noqa:F403


# APP CONFIGURATION

# Turn debug off so tests run faster
DEBUG = False
TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG


# CACHING CONFIGURATION

# Speed advantages of in-memory caching without having to run Memcached
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache", "LOCATION": ""}}


# AUTH SETTINGS, PASSWORD STORAGE/VALIDATION, OAUTH2

# Use fast password hasher so tests run faster
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

TESTING = env.bool("TESTING", default=True)
