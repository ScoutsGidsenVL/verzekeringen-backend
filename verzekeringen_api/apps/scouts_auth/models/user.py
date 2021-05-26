from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.AutoField(primary_key=True, editable=False)
    group_admin_id = models.CharField(db_column="ga_id", max_length=255, blank=True)

    # Fields that arent saved in database but just kept in memory
    birth_date: datetime.date
    membership_number: str
    scouts_groups: list = []
