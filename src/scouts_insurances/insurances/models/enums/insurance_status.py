from django.db import models


class InsuranceStatus(models.IntegerChoices):
    NEW = 10, "Nieuw"
    ACCEPTED = 20, "Goedgekeurd"
    BILLED = 30, "Gefactureerd"
    WAITING = 40, "In wacht"
    REJECTED = 99, "Afgekeurd"
