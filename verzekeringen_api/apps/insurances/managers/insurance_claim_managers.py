from django.conf import settings
from django.db import models


class InsuranceClaimQuerySet(models.QuerySet):
    def allowed(self, user: settings.AUTH_USER_MODEL):
        pass
    
    def allowed_for_section_leaders(self, user: settings.AUTH_USER_MODEL):
        pass
    
    def allowed_for_group_leaders(self, user: settings.AUTH_USER_MODEL):
        pass
    
    def allowed_for_administrators(self, user: settings.AUTH_USER_MODEL):
        pass


class InsuranceClaimManager(models.Manager):
    def get_queryset(self):
        return InsuranceClaimQuerySet(self.model, using=self._db)