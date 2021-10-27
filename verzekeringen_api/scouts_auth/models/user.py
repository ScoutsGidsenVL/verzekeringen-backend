import logging, uuid
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone

from scouts_auth.models.value_objects import partial_scouts_group


logger = logging.getLogger(__name__)


class User(AbstractUser):
    id = models.AutoField(primary_key=True, editable=False)
    uuid = models.UUIDField(
        primary_key=False, editable=False, default=uuid.uuid4, unique=True
    )
    # The scout id in group admin
    group_admin_id = models.CharField(blank=True, db_column="ga_id", max_length=255)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(
        max_length=150, unique=True, validators=[UnicodeUsernameValidator]
    )
    first_name = models.CharField(blank=True, max_length=150)
    last_name = models.CharField(blank=True, max_length=150)
    email = models.EmailField(blank=True, max_length=254)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    groups = models.ManyToManyField(
        blank=True,
        related_name="user_groups",
        related_query_name="user",
        to="auth.Group",
    )
    user_permissions = models.ManyToManyField(
        blank=True,
        related_name="user_permissions",
        related_query_name="user",
        to="auth.Permission",
    )

    # Fields that arent saved in database but just kept in memory:

    # The scout birth date
    birth_date: datetime.date = None
    # The scout membership number, provided by group admin
    membership_number: str = ""
    # The scout cell phone number
    phone_number: str = ""
    # The active access token, provided by group admin oidc
    access_token: str = ""
    # The partial groups are always filled in, but don't include extra data
    # This extra data can be gotten by calling fetch_detailed_group_info
    partial_scouts_groups: list = []
    scouts_groups: list = []

    class Meta:
        permissions = (("access_disabled_entities", "Access disabled entities"),)

    def __str__(self):
        return ("User object: \
            id(%s), \
            uuid(%s), \
            username(%s), \
            email(%s), \
            first_name(%s), \
            last_name(%s), \
            group_admin_id(%s), \
            is_superuser(%s), \
            is_staff(%s), \
            is_active(%s), \
            last_login(%s), \
            date_joined(%s), \
            groups(%s), \
            partial_scouts_groups(%s), \
            scouts_groups(%s)",
            str(self.id), str(self.uuid), str(self.username), str(self.email), str(self.first_name),
            str(self.last_name), str(self.group_admin_id), str(self.is_superuser),
            str(self.is_staff), str(self.is_active), str(self.last_login), str(self.date_joined),
            (", ".join(self.groups) if self.groups and isinstance(self.groups, list) else "[]"),
            (", ".join(self.partial_scouts_groups) if self.partial_scouts_groups and isinstance(self.scouts_groups, list) else "[]"),
            (", ".join(self.scouts_groups) if self.scouts_groups and isinstance(self.scouts_groups, list) else "[]"))

    def fetch_detailed_group_info(self):
        # Importing here, to avoid a circular import error
        from scouts_auth.services import GroupAdminGroupService

        groups = dict()
        group_links = []
        # refs: #79675 - distinct members groups
        for partial_group in self.partial_scouts_groups:
            group_links.append(partial_group.href)

            if not partial_group in groups:
                groups[partial_group.id] = GroupAdminGroupService().get_detailed_group(
                    partial_group
                )
        self.scouts_groups = groups.values()
        self.partial_scouts_groups = group_links
