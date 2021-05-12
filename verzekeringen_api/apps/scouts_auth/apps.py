from django.apps import AppConfig
from django.db.models.signals import post_migrate


class AuthConfig(AppConfig):
    name = "apps.scouts_auth"

    def ready(self):
        # Need to import here because importing above will lead to AppRegistryNotReady exception
        from .signals import populate_groups

        post_migrate.connect(populate_groups, sender=self)
