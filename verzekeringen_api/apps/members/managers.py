from django.db import models


class InuitsNonMemberQuerySet(models.QuerySet):
    def allowed(self, user):
        user_group_ids = [group.id for group in user.partial_scouts_groups]
        return self.filter(group_number__in=user_group_ids)


class InuitsNonMemberManager(models.Manager):
    def get_queryset(self):
        return InuitsNonMemberQuerySet(self.model, using=self._db)
