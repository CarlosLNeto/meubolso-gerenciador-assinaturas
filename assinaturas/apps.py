from django.apps import AppConfig


class AssinaturasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'assinaturas'

    def ready(self):
        """Importa os signals quando a aplicação está pronta"""
        import assinaturas.signals
