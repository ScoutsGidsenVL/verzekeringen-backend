from django.db import models


class CountryQuerySet(models.QuerySet):
    def by_type(self, type_id):
        return self.filter(insurance_types__id=type_id)

    def by_types(self, type_id_list):
        return self.filter(insurance_types__id__in=type_id_list).distinct()


class CountryManager(models.Manager):
    def get_queryset(self):
        return CountryQuerySet(self.model, using=self._db)

    def by_type(self, type_id):
        return self.get_queryset().by_type(type_id)

    def by_types(self, type_id_list):
        return self.get_queryset().by_types(type_id_list)
