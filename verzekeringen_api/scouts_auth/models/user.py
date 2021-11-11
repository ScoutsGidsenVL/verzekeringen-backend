import logging, uuid
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone


logger = logging.getLogger(__name__)


class User(AbstractUser):
    #
    # PRIMARY KEY (uuid)
    #
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, unique=True)

    #
    # Fields inherited from django.contrib.auth.models.AbstractUser
    #
    username = models.CharField(
        name="username",
        max_length=150,
        unique=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        validators=[UnicodeUsernameValidator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )
    first_name = models.CharField(name="first name", max_length=150, blank=True)
    last_name = models.CharField(name="last name", max_length=150, blank=True)
    email = models.EmailField(name="email address", blank=True)
    is_staff = models.BooleanField(
        name="staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(
        name="active",
        default=True,
        help_text="Designates whether this user should be treated as active. "
        "Unselect this instead of deleting accounts.",
    )
    date_joined = models.DateTimeField(name="date joined", default=timezone.now)

    #
    # Fields inherited from django.contrib.auth.AbstractBaseUser
    #
    password = models.CharField(name="password", max_length=128)
    last_login = models.DateTimeField(name="last login", blank=True, null=True)

    #
    # Fields inherited from django.contrib.auth.models.PermissionsMixin
    #
    is_superuser = models.BooleanField(
        name="superuser status",
        default=False,
        help_text="Designates that this user has all permissions without " "explicitly assigning them.",
    )
    groups = models.ManyToManyField(
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions "
        "granted to each of their groups.",
        related_name="user_groups",
        related_query_name="user",
        to="auth.group",
    )
    user_permissions = models.ManyToManyField(
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="user_permissions",
        related_query_name="user",
        to="auth.permission",
    )

    class Meta:
        permissions = (("access_disabled_entities", "Access disabled entities"),)
        abstract = True

    def __str__(self):
        return "id({}), username({}), first_name({}), last_name({}), email({}), is_staff({}), is_active({}), date_joined({}), last_login({}), is_superuser({}), groups({}), user_permissions({})".format(
            str(self.id),
            str(self.username),
            str(self.first_name),
            str(self.last_name),
            str(self.email),
            str(self.is_staff),
            str(self.is_active),
            str(self.date_joined),
            str(self.last_login),
            str(self.is_superuser),
            ", ".join(self.groups) if self.groups and isinstance(self.groups, list) else "[]",
            ", ".join(str(permission) for permission in self.permissions),
        )
