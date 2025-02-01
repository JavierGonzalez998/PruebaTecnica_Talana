from django.apps import AppConfig
class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userService'

    def ready(self):
        import userService.signals 