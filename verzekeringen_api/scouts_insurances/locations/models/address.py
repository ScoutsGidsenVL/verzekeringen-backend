from django.db import models


class Address(models.Model):

    id = models.AutoField(db_column="adres_id", primary_key=True)
    street = models.CharField(db_column="straat", max_length=100)
    number = models.CharField(db_column="nummer", max_length=5)
    letter_box = models.CharField(db_column="bus", max_length=5, null=True, blank=True)
    postal_code = models.CharField(db_column="postcode", max_length=4)
    city = models.CharField(db_column="gemeente", max_length=40)

    class Meta:
        db_table = "vrzk_adres"
        managed = False
