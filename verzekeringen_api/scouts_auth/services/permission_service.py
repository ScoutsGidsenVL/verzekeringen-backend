import logging, yaml, importlib

from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ObjectDoesNotExist

from scouts_auth.util import SettingsHelper


logger = logging.getLogger(__name__)


class PermissionService:
    def _add_permission_by_name(self, group, permission_name):
        try:
            permission_name = permission_name.split(".")
            permission = Permission.objects.get(
                codename=permission_name[1], content_type__app_label=permission_name[0]
            )
            group.permissions.add(permission)
        except ObjectDoesNotExist:
            logger.error("Permission %s doesn't exist", permission_name)

    def populate_roles(self, sender, **kwargs):
        # Will populate groups and add permissions to them, won't create permissions
        # these need to be created in models
        import importlib.resources as pkg_resources

        roles_package = SettingsHelper.get_authorization_roles_config_package()
        roles_yaml = SettingsHelper.get_authorization_roles_config_yaml()

        logger.debug(
            "SCOUTS_AUTH: importing roles and permissions from %s/%s",
            roles_package,
            roles_yaml,
        )

        importlib.import_module(roles_package)
        yaml_data = pkg_resources.read_text(roles_package, roles_yaml)

        try:
            groups = yaml.safe_load(yaml_data)
            for group_name, permissions in groups.items():
                group = Group.objects.get_or_create(name=group_name)[0]
                group.permissions.clear()
                for permission_name in permissions:
                    self._add_permission_by_name(group, permission_name)
                group.save()
        except yaml.YamlError as exc:
            logger.error("Error while importing permissions groups", exc)
