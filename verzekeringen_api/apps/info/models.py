from decimal import Decimal
from django.db import models


class InfoVariable(models.Model):
    key = models.CharField(max_length=30, primary_key=True)
    # Value field will contain html that will be directly used in frontend
    value = models.TextField()
