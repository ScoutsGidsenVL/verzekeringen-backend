from django.conf import settings
from django.db import models
from django.db.models import Q


class EquipmentQuerySet(models.QuerySet):
    def template_editable(self, user: settings.AUTH_USER_MODEL):
        return self.filter(Q(template__editable=True))

    def editable(self, user: settings.AUTH_USER_MODEL):
        from scouts_insurances.insurances.models.enums import InsuranceStatus

        return self.filter(Q(insurance___status__in=[InsuranceStatus.NEW, InsuranceStatus.WAITING]))

    def non_editable(self, user: settings.AUTH_USER_MODEL):
        from scouts_insurances.insurances.models.enums import InsuranceStatus

        return self.filter(
            Q(
                insurance___status__in=[
                    InsuranceStatus.ACCEPTED,
                    InsuranceStatus.BILLED,
                    InsuranceStatus.WAITING,
                ]
            )
        )


class EquipmentManager(models.Manager):
    def get_queryset(self):
        return EquipmentQuerySet(self.model, using=self._db)
