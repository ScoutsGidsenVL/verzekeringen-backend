from inuits.models import AbstractBaseModel
from inuits.mixins import AuditUserModelMixin, AuditTimestampModelMixin


class AuditedBaseModel(AuditUserModelMixin, AuditTimestampModelMixin, AbstractBaseModel):
    """Abstract base models that logs create and update events for time and user."""

    class Meta:
        abstract = True
