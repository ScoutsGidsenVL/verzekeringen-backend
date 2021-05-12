from rest_framework import permissions


class ExtendedDjangoModelPermissions(permissions.DjangoModelPermissions):
    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": [],
        "HEAD": [],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }


class CustomDjangoPermission(permissions.BasePermission):
    permission_name = None

    def __init__(self, permission_name):
        self.permission_name = permission_name

    def has_permission(self, request, view):
        return request.user.has_perm(self.permission_name)
