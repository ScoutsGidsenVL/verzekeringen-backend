from scouts_auth.inuits.mixins import AuditTimestampModelMixin, AuditUserModelMixin
from scouts_auth.inuits.models import AbstractBaseModel


class AuditedBaseModel(AuditUserModelMixin, AuditTimestampModelMixin, AbstractBaseModel):
    """Abstract base models that logs create and update events for time and user."""

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
