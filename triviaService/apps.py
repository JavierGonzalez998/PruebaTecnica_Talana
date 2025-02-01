from django.apps import AppConfig


class TriviaserviceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'triviaService'
    def ready(self):
        import triviaService.signals 