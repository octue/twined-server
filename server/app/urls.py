import json
import os
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView
from reel import urls as reel_urls

from .context_processors import app_rendering_ctx


class ReactView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(ReactView, self).get_context_data(**kwargs)
        context["ctx"] = json.dumps(app_rendering_ctx())
        return context


def dev_context(request):
    """ Return with json application context and supplied csrf token. DEBUG mode only (**SECURITY**).

    React development uses npm run start; so you're running a second server which hot reloads react.
    This is great for development, but it doesn't actually render the page template from django, so context variables
    appear as a raw template string: '{{ ctx|safe }}', and the CSRF token cookie doesn't get set.

    This endpoint responds in DEBUG mode only (because returning csrf token on an unprotected endpoint in production
    would be BAD) with the required context so a hot reloaded site can function as if the template were rendered by
    django.

    """
    if settings.DEBUG:
        return JsonResponse({"csrf": get_token(request), "ctx": app_rendering_ctx()})
    raise Exception("dev_context endpoint should only be accessed in DEBUG mode as it is not secure.")


urlpatterns = [
    url(r"^robots.txt$", lambda r: HttpResponse("User-agent: *\nDisallow:", content_type="text/plain")),
    url(r"", include(reel_urls)),
]

# Serve the built frontend app assets
urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.REACT_BUILD_DIR, "build", "static"))


# Add development context in debug mode only
if settings.DEBUG:
    urlpatterns += [url(r"^dev_context/", dev_context)]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Frontend - Catch-all URL
# On any other url, including root, serve up the react-app and let react router take care of nav
#   Note for local development:
#       In hot-reload mode, the app is served on localhost:3000/
#       This is served by npm, not by django, so you'll be unable to access the django-served
#       routes like /admin/. To develop and preview on those routes, use localhost:8000/
urlpatterns += [
    url(
        r"^.*",
        ensure_csrf_cookie(ReactView.as_view(template_name=os.path.join(settings.REACT_BUILD_DIR, "index.html"))),
    )
]
