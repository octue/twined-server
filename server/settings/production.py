from .base import *  # noqa:F403


# DIRECTORIES AND ENVIRONMENT


# APP CONFIGURATION

# Always set to false in production
DEBUG = False

# Raises ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env("SECRET_KEY")


# MIDDLEWARE CONFIGURATION


# SECURITY CONFIGURATION
# This ensures that Django will use only https requests and be able to detect a secure connection properly on Heroku
# See:
#   https://help.heroku.com/J2R1S4T8/can-heroku-force-an-application-to-use-ssl-tls
#   https://docs.djangoproject.com/en/dev/ref/middleware/#module-django.middleware.security
#   https://docs.djangoproject.com/en/dev/howto/deployment/checklist/#run-manage-py-check-deploy
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool("DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True)
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SECURE_SSL_REDIRECT = True
# CSRF_COOKIE_SECURE = True
# CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "DENY"


# CACHING CONFIGURATION

# Use redis for caching in production (requires the location, not just the url)
# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': REDIS_LOCATION,
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#             'IGNORE_EXCEPTIONS': True,  # mimics memcache behavior.
#                                         # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
#         }
#     }
# }

# INTERNATIONALISATION


# TEMPLATE CONFIGURATION


# STATIC FILES

# Serve compressed and cached static files
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# TESTING

# Always turn testing off in production
TESTING = False
TESTING_EXPENSIVE = False


# LOGGING


# INTEGRATIONS - GOOGLE
