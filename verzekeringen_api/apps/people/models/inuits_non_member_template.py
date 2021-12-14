from django.db import models

from apps.people.models import InuitsNonMember

from scouts_insurances.people.models import NonMember


class InuitsNonMemberTemplate(models.Model):
    non_member = models.OneToOneField(
        NonMember, on_delete=models.CASCADE, primary_key=True, db_constraint=models.UniqueConstraint
    )
    inuits_non_member = models.ForeignKey(InuitsNonMember, on_delete=models.CASCADE, related_name="template")
