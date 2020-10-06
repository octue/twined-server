from django.apps import AppConfig


class GitbotAppConfig(AppConfig):
    name = "gitbot"
    verbose_name = "Gitbot (handles fetching stuff from git)"

    def ready(self):
        import gitbot.signals  # noqa: F401
