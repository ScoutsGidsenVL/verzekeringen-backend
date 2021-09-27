import logging
from django.db import models

logger = logging.getLogger(__name__)


class Sex(models.TextChoices):
    # alphabetically ordered
    FEMALE = "F", "Female"
    MALE = "M", "Male"
    OTHER = "O", "Other"
    UNKNOWN = "U", "Unknown"


class SexHelper:
    @staticmethod
    def parse_sex(value) -> Sex:
        if not value:
            return Sex.UNKNOWN

        value = value.strip().upper()
        if value in ("O", "OTHER", "ANDERE"):
            return Sex.OTHER
        if value in ("F", "FEMALE", "V", "VROUW"):
            return Sex.FEMALE
        if value in ("M", "MALE", "MAN"):
            return Sex.MALE

        return Sex.UNKNOWN
