import logging

from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

logger = logging.getLogger(__name__)


class InsuranceClaimsPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return True
        # if request.user.has_role_administrator():
        #     return True
        # raise PermissionDenied({"message":"You don't have permission to access",
        #                         "object_id": obj.id})

