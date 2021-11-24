from django.db import models

from apps.insurances.models.base_insurance import BaseInsurance
from apps.insurances.models.enums import EventSize

from groupadmin.models import PostcodeCity


class EventInsurance(BaseInsurance):
    insurance_parent = models.OneToOneField(
        BaseInsurance,
        db_column="verzekeringsid",
        on_delete=models.CASCADE,
        parent_link=True,
        primary_key=True,
        related_name="event_child",
    )
    nature = models.CharField(db_column="aardactiviteit", max_length=500)
    event_size = models.IntegerField(db_column="aantbezoekers", null=True, choices=EventSize.choices)
    postcode = models.IntegerField(db_column="postcode", null=True)
    city = models.CharField(db_column="gemeente", max_length=40)

    class Meta:
        db_table = "vrzktypeevenement"
        managed = False

    @property
    def postcode_city(self):
        return PostcodeCity(postcode=self.postcode, name=self.city)

    def has_attachment(self) -> bool:
        return self.attachment is not None
