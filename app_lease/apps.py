from django.apps import AppConfig


class AppLeaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_lease'

    def ready(self):
        import app_lease.signals
