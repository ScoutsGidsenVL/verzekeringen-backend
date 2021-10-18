from django.db import models
from django.conf import settings

from apps.insurances.models import InsuranceType


class InsuranceDraftQuerySet(models.QuerySet):
    def allowed(self, user):
        return self.filter(created_by=user)


class InsuranceDraftManager(models.Manager):
    def get_queryset(self):
        return InsuranceDraftQuerySet(self.model, using=self._db)


class InsuranceDraft(models.Model):
    objects = InsuranceDraftManager()

    id = models.AutoField(primary_key=True)
    created_on = models.DateTimeField(auto_now_add=True)
    data = models.JSONField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Created by",
        blank=True,
        null=True,
        related_name="insurance_draft_created",
        on_delete=models.SET_NULL,
    )
    insurance_type = models.ForeignKey(InsuranceType, related_name="insurance_drafts", on_delete=models.RESTRICT)
