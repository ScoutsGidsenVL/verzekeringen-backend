from django.db import models

from apps.people.managers import InuitsNonMemberTemplateManager
from apps.people.models import InuitsNonMember

from scouts_insurances.people.models import NonMember


class InuitsNonMemberTemplate(models.Model):
    objects = InuitsNonMemberTemplateManager()

    non_member = models.OneToOneField(
        NonMember,
        on_delete=models.CASCADE,
        primary_key=True,
        db_constraint=models.UniqueConstraint,
        related_name="template",
    )
    inuits_non_member = models.ForeignKey(InuitsNonMember, on_delete=models.CASCADE, related_name="template")

    # Convenience field to indicate wether a NonMember can be edited
    editable = models.BooleanField(default=True)
