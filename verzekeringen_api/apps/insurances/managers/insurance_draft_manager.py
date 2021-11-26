from django.db import models


class InsuranceDraftQuerySet(models.QuerySet):
    def allowed(self, user):
        return self.filter(created_by=user)


class InsuranceDraftManager(models.Manager):
    def get_queryset(self):
        return InsuranceDraftQuerySet(self.model, using=self._db)
