from django.urls import path

from .consumers import AnalysisConsumer, ServiceConsumer


websocket_urlpatterns = [
    path(r"ws/service/", ServiceConsumer),
    path(r"ws/analyses/", AnalysisConsumer),
    path(r"ws/analyses/<uuid:analysis_id>/", AnalysisConsumer),
]
