from django.apps import AppConfig


class ReelAppConfig(AppConfig):
    name = "reel"
    verbose_name = "Reel (handles twines)"

    def ready(self):
        import reel.signals  # noqa: F401
