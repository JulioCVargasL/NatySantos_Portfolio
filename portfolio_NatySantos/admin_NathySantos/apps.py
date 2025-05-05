from django.apps import AppConfig


class AdminNathysantosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_NathySantos'

    def ready(self):
      import admin_NathySantos.signals