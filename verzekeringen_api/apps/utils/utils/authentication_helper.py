"""apps.utils.authentication_helper."""
import logging
import typing as tp

from django.conf import settings
from rest_framework.exceptions import PermissionDenied

from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)

class AuthenticationHelper:
    
    @staticmethod
    def load_groups(user: settings.AUTH_USER_MODEL) -> tp.List[str]:
        groups: str = []
        for group in user.scouts_groups: 
            groups.append(group.number)
        
        return groups

    @staticmethod
    def has_rights_for_group(user: settings.AUTH_USER_MODEL, group_admin_id: str = None) -> bool: 
        # logger.debug('groups: ', AuthenticationHelper.load_groups(user=user))
        if not group_admin_id in AuthenticationHelper.load_groups(user=user):
            raise PermissionDenied(
                {
                    "message": f"You don't have permission to this request for group {group_admin_id}"

                }
            )

        return True