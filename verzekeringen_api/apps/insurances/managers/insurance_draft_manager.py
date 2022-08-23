from django.db import models


class InsuranceDraftQuerySet(models.QuerySet):
    def allowed(self, user):

        user_groups = list()
        for scouts_group in user.scouts_groups:
            user_groups.append(scouts_group.number)

        return self.filter(data__scouts_group__group_admin_id__in=user_groups)

class InsuranceDraftManager(models.Manager):
    def get_queryset(self):
        return InsuranceDraftQuerySet(self.model, using=self._db)
