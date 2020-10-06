import json
import os
from django.conf import settings
from django.conf.urls import include, url
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView
from reel import urls as reel_urls

from .context_processors import app_rendering_ctx


class ReactView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(ReactView, self).get_context_data(**kwargs)
        context["ctx"] = json.dumps(app_rendering_ctx())
        return context


urlpatterns = [
    url(r"^robots.txt$", lambda r: HttpResponse("User-agent: *\nDisallow:", content_type="text/plain")),
    url(r"", include(reel_urls)),
]


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
