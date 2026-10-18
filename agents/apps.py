from django.apps import AppConfig

class AgentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'agents'

    def ready(self):
        # This line is crucial; it imports your signals so they are registered
        import agents.signals