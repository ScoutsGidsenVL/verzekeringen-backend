from django.db import models

from scouts_auth.inuits.models.fields import OptionalTextField
from scouts_auth.inuits.utils import TextUtils


class Linkable(models.Model):

    link = OptionalTextField()

    class Meta:
        abstract = True

    def has_link(self) -> bool:
        return TextUtils.is_non_empty(self.link)
