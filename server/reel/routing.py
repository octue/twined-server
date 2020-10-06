from channels.routing import URLRouter
from django.urls import path

from .consumers import AnalysisConsumer, ServiceConsumer


router = URLRouter(
    [
        path(r"ws/service/", ServiceConsumer),
        path(r"ws/analyses/", AnalysisConsumer),
        path(r"ws/analyses/<uuid:analysis_id>/", AnalysisConsumer),
    ]
)
