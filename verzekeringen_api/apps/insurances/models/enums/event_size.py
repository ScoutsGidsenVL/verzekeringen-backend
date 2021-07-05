from django.db import models


class EventSize(models.IntegerChoices):
    FIVEHUNDRED = 1, "1-500 (65,55 eur/dag)"
    THOUSAND = 2, "500-1000 (131,10 eur/dag)"
    THOUSANDFIVEHUNDRED = 3, "1000-1500 (163,88 eur/dag)"
    TWOTHOUSAND = 4, "1500-2500 (229,43 eur/dag)"
    TWOTHOUSANDFIVEHUNDRED = 5, "meer dan 2500 (in overleg met Ethias)"
