import logging

from scouts_auth.signals import app_ready, authenticated


logger = logging.getLogger(__name__)


class ScoutsAuthSignalHandler:
    """
    A class to allow dependent packages to act on events in the authentication flow.

    @see https://docs.djangoproject.com/en/3.2/topics/signals/
    """

    # SINGLETON
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(ScoutsAuthSignalHandler, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    # END SINGLETON

    # def app_ready(self, sender, **kwargs):
    #     from scouts_auth.services import PermissionService

    #     logger.debug("SCOUTS_AUTH: Populating permissions groups")
    #     post_migrate.connect(PermissionService().populate_roles, sender=self)

    # def authenticated(self, sender, **kwargs):
    #     logger.debug("SCOUTS-AUTH: User is authenticated")

    def app_ready(self):
        logger.debug("SCOUTS-AUTH: Application is ready")
        app_ready.send(sender=self.__class__)
        from scouts_auth.services import PermissionService
        from django.db.models.signals import post_migrate

        logger.debug("SCOUTS_AUTH: Populating permissions groups")
        PermissionService().populate_roles()

    def authenticated(self, user=None, token: str = None):
        logger.debug("SCOUTS-AUTH: user authenticated")
        authenticated.send(sender=self.__class__)
