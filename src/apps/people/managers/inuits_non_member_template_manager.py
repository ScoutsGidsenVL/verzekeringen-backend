from django.db import models
from django.db.models import Q


class InuitsNonMemberTemplateQuerySet(models.QuerySet):
    def editable(self, inuits_non_member=None):
        if not inuits_non_member:
            return self.filter(editable=True)

        return self.filter(Q(editable=True) & Q(inuits_non_member=inuits_non_member))


class InuitsNonMemberTemplateManager(models.Manager):
    def get_queryset(self):
        return InuitsNonMemberTemplateQuerySet(self.model, using=self._db)
