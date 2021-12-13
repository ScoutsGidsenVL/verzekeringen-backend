import logging

from django.db import models


logger = logging.getLogger(__name__)


class InfoVariableQuerySet(models.QuerySet):
    def get_variable(self, key: str):
        logger.debug("COST: Fetching info variable with key %s", key)
        return self.get(key=key)


class InfoVariableManager(models.Manager):
    def get_queryset(self):
        return InfoVariableQuerySet(self.model, using=self._db)

    def get_variable(self, key: str):
        return self.get_queryset().get_variable(key)


class InfoVariable(models.Model):
    objects = InfoVariableManager()

    key = models.CharField(max_length=30, primary_key=True)
    # Value field will contain html that will be directly used in frontend
    value = models.TextField()
