import logging

from django.db import models

from rest_framework import serializers


logger = logging.getLogger(__name__)


class Gender(models.TextChoices):
    # alphabetically ordered
    FEMALE = "F", "Female"
    MALE = "M", "Male"
    OTHER = "O", "Other"
    UNKNOWN = "U", "Unknown"


class GenderHelper:
    @staticmethod
    def parse_gender(value) -> Gender:
        if not value:
            return Gender.UNKNOWN

        value = value.strip().upper()
        if value in ["O", "OTHER", "ANDERE"]:
            return Gender.OTHER
        if value in ["F", "FEMALE", "V", "VROUW"]:
            return Gender.FEMALE
        if value in ["M", "MALE", "MAN"]:
            return Gender.MALE

        return Gender.UNKNOWN

