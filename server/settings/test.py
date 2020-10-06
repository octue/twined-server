from .base import *  # noqa:F403


# APP CONFIGURATION

# Turn debug off so tests run faster
DEBUG = False
TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG

# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development! Using this key in production is insecure!
SECRET_KEY = env("DJANGO_SECRET_KEY", default="`c}ycP0(JRg*azi<<|=8d>?vH#@xI:P?Yksdc?Zog$~WZHw|oi")


# CACHING CONFIGURATION

# Speed advantages of in-memory caching without having to run Memcached
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache", "LOCATION": ""}}


# AUTH SETTINGS, PASSWORD STORAGE/VALIDATION, OAUTH2

# Use fast password hasher so tests run faster
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

TESTING = env.bool("TESTING", default=True)

DRAMATIQ_BROKER = {
    "BROKER": "dramatiq.brokers.stub.StubBroker",
    "OPTIONS": {},
    "MIDDLEWARE": [
        "dramatiq.middleware.AgeLimit",
        "dramatiq.middleware.TimeLimit",
        "dramatiq.middleware.Callbacks",
        "dramatiq.middleware.Pipelines",
        "dramatiq.middleware.Retries",
    ],
}
