from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from ..services import GroupAdminService


class User(AbstractUser):
    id = models.AutoField(primary_key=True, editable=False)
    group_admin_id = models.CharField(db_column="ga_id", max_length=255, blank=True)

    # Fields that arent saved in database but just kept in memory
    birth_date: datetime.date
    membership_number: str
    phone_number: str
    access_token: str
    # The partial groups are always filled in but do not include some extra data
    # This extra data can be gotten by calling the fetch_detailed_group_info method
    partial_scouts_groups: list = []
    scouts_groups: list = []

    def fetch_detailed_group_info(self):
        detailed_groups = dict()
        # refs: #79675 - distinct members groups
        for partial_group in self.partial_scouts_groups:
            if not partial_group in detailed_groups:
                detailed_groups[partial_group.id] = GroupAdminService.get_detailed_group_info(partial_group)
        self.scouts_groups = detailed_groups.values()
