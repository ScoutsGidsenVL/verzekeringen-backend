from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import os
import yaml


def _add_permission_by_name(group, permission_name):
    try:
        permission_name = permission_name.split(".")
        permission = Permission.objects.get(codename=permission_name[1], content_type__app_label=permission_name[0])
        group.permissions.add(permission)
    except ObjectDoesNotExist as exc:
        print("Permission %s doesn't exist" % permission_name)


def populate_groups(sender, **kwargs):
    # Will populate groups and add permissions to it, won't create permissions these need to be created in models
    yaml_path = os.path.join(settings.BASE_DIR, "apps/scouts_auth/initial_data/groups.yaml")

    with open(yaml_path, "r") as stream:
        try:
            groups = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    for group_name, permissions in groups.items():
        group = Group.objects.get_or_create(name=group_name)[0]
        group.permissions.clear()
        for permission_name in permissions:
            _add_permission_by_name(group, permission_name)
        group.save()
