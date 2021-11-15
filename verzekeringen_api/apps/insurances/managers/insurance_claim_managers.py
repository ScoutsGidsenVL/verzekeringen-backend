from django.db import models

from groupadmin.models import ScoutsUser


class InsuranceClaimQuerySet(models.QuerySet):
    def allowed(self, user: ScoutsUser):
        pass


class InsuranceClaimManager(models.Manager):
    def get_queryset(self):
        return InsuranceClaimQuerySet(self.model, using=self._db)
