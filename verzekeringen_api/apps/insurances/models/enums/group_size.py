from django.db import models


class GroupSize(models.IntegerChoices):
    FIFTY = 1, "1-50"
    HUNDRED = 2, "51-100"
    HUNDREDFIFTY = 3, "101-150"
    TWOHUNDRED = 4, "151-200"
    TWOHUNDREDFIFTY = 5, "201-250"
    THREEHUNDRED = 6, "251-300"
    THREEHUNDREDFIFTY = 7, "301-350"
    FOURHUNDRED = 8, "351-400"
    FOURHUNDREDFIFTY = 9, "401-450"
