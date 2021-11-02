from django.db import models


class AbstractModel(models.Model):
    class Meta:
        abstract = True
