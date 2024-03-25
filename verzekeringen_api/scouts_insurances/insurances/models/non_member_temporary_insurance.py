from django.db import models

from scouts_insurances.insurances.models import TemporaryInsurance
from scouts_insurances.people.models import NonMember


class NonMemberTemporaryInsurance(models.Model):
    non_member_id = models.ForeignKey(
        NonMember, db_column="nietledenid", on_delete=models.CASCADE, primary_key=True, related_name="temporary"
    )
    temporary_insurance = models.ForeignKey(TemporaryInsurance, db_column="verzekeringsid", on_delete=models.CASCADE)

    class Meta:
        db_table = "vrzknietledentijd"
        managed = False
