from .base import *  # noqa:F403


# APP CONFIGURATION

DEBUG = env.bool("DJANGO_DEBUG", default=True)
TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG

# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development! Using this key in production is insecure!
SECRET_KEY = env("DJANGO_SECRET_KEY", default="`c}ycP0(JRg*azi<<|=8d>?vH#@xI:P?Yksdc?Zog$~WZHw|oi")


# CACHING CONFIGURATION

CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache", "LOCATION": ""}}


# TESTING
TEST_RUNNER = "django.test.runner.DiscoverRunner"
TESTING = env.bool("TESTING", default=True)
