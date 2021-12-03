import logging
from typing import List

from django.db import models

from scouts_insurances.insurances.models import InsuranceType


logger = logging.getLogger(__name__)


class CountryQuerySet(models.QuerySet):
    def by_insurance_type(self, insurance_type: InsuranceType):
        return self.by_insurance_type_id(insurance_type.id)

    def by_insurance_type_id(self, insurance_type_id: int):
        return self.filter(insurance_types__id=insurance_type_id)

    def by_insurance_types(self, insurance_types: List[InsuranceType]):
        return self.by_insurance_type_ids([insurance_type.id for insurance_type in insurance_types])

    def by_insurance_type_ids(self, type_id_list: List[int]):
        return self.filter(insurance_types__id__in=type_id_list).distinct()

    def by_name(self, country_name: str):
        logger.debug("Querying db for country with name %s", country_name)
        return self.get(name=country_name)


class CountryManager(models.Manager):
    def get_queryset(self):
        return CountryQuerySet(self.model, using=self._db)

    def by_insurance_type(self, insurance_type: InsuranceType):
        return self.get_queryset().by_insurance_type(insurance_type)

    def by_insurance_type_id(self, type_id: int):
        return self.get_queryset().by_insurance_type_id(type_id)

    def by_insurance_types(self, insurance_types: List[InsuranceType]):
        return self.get_queryset().by_insurance_types(insurance_types)

    def by_insurance_type_ids(self, type_id_list: List[int]):
        return self.get_queryset().by_insurance_type_ids(type_id_list)

    def by_name(self, country_name: str):
        return self.get_queryset().by_name(country_name)
