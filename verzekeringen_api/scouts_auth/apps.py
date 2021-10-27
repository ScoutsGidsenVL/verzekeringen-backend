import logging


from django.apps import AppConfig
from django.db.models.signals import post_migrate


logger = logging.getLogger(__name__)


class ScoutsAuthConfig(AppConfig):
    name = "scouts_auth"

    def ready(self):
        from scouts_auth.services import PermissionService

        logger.debug("SCOUTS_AUTH: Populating permissions groups")
        post_migrate.connect(PermissionService().populate_roles, sender=self)
