from django.db import migrations

# Roles that are no longer assigned or only granted permissions every user already has (T7607).
# They were removed from roles.yaml at the same time, so PermissionService.populate_roles() won't recreate them.
UNUSED_ROLES = ["role_district_commissioner", "role_group_leader"]


def remove_unused_roles(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    # delete() also removes the links to users and permissions
    Group.objects.filter(name__in=UNUSED_ROLES).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("scouts_auth", "0004_alter_persistedfile_created_by_and_more"),
    ]

    # No reverse: restoring the roles in roles.yaml recreates them at startup, the links to users are not restored
    operations = [migrations.RunPython(remove_unused_roles, migrations.RunPython.noop)]
