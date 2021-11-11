import logging

from django.conf import settings
from django.dispatch import receiver

from scouts_auth.signals import ScoutsAuthSignalSender, app_ready, authenticated
from scouts_auth.services import PermissionService

from groupadmin.models import ScoutsUser
from groupadmin.services import GroupAdmin


logger = logging.getLogger(__name__)


class InsuranceSignalHandler:
    @staticmethod
    @receiver(app_ready, sender=ScoutsAuthSignalSender.sender, dispatch_uid=ScoutsAuthSignalSender.app_ready_uid)
    def handle_app_ready(**kwargs):
        logger.debug("SIGNAL received: 'app_ready' from %s", ScoutsAuthSignalSender.sender)

        try:
            PermissionService().populate_roles()
        except Exception as exc:
            logger.error("Unable to populate user roles", exc)

    @staticmethod
    @receiver(
        authenticated, sender=ScoutsAuthSignalSender.sender, dispatch_uid=ScoutsAuthSignalSender.authenticated_uid
    )
    def handle_authenticated(user: settings.AUTH_USER_MODEL, **kwargs):
        logger.debug("SIGNAL received: 'authenticated' from %s", ScoutsAuthSignalSender.sender)

        updated_user: settings.AUTH_USER_MODEL = GroupAdmin().get_member_profile(active_user=user)

        user.group_admin_id = updated_user.group_admin_id
        user.gender = updated_user.gender
        user.phone = updated_user.phone
        user.membership_number = updated_user.membership_number
        user.customer_number = updated_user.customer_number
        user.birth_date = updated_user.birth_date
        user.first_name = updated_user.first_name
        user.last_name = updated_user.last_name
        user.email = updated_user.email

        user.save()

        return user
