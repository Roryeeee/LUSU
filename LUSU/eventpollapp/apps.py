from django.apps import AppConfig


class EventpollappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eventpollapp'

class YourAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'your_app'

    def ready(self):
        import your_app.signals