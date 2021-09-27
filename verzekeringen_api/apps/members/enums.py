from django.db import models


class Sex(models.TextChoices):
    # alphabetically ordered
    FEMALE = "F", "Female"
    MALE = "M", "Male"
    OTHER = "O", "Other"
    UNKNOWN = "U", "Unknown"
