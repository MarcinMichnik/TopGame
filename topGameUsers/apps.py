from django.apps import AppConfig


class TopgameusersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'topGameUsers'

    def ready(self):
        import topGameUsers.signals