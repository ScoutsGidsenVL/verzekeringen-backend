from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.members.models import NonMember
from .base_insurance import BaseInsurance


class TemporaryInsurance(BaseInsurance):
    insurance_parent = models.OneToOneField(
        BaseInsurance,
        db_column="verzekeringsid",
        on_delete=models.CASCADE,
        parent_link=True,
        primary_key=True,
        related_name="temporary_child",
    )
    nature = models.CharField(db_column="aardactiviteit", max_length=500)
    postcode = models.IntegerField(db_column="postcode", null=True, blank=True)
    city = models.CharField(db_column="gemeente", max_length=40, blank=True)
    country = models.CharField(db_column="land", max_length=45, blank=True)

    non_members = models.ManyToManyField(
        NonMember, through="NonMemberTemporaryInsurance", related_name="temporary_insurances"
    )

    class Meta:
        db_table = "vrzktypetijdact"
        managed = False

    def clean(self):
        super().clean()
        if self.country and (self.postcode or self.city):
            raise ValidationError("If country given then postcode and city cannot be given")
        elif not self.country and ((self.postcode and not self.city) or (self.city and not self.postcode)):
            raise ValidationError("When no country given both city and postcode are required")


class NonMemberTemporaryInsurance(models.Model):
    non_member_id = models.ForeignKey(NonMember, db_column="nietledenid", on_delete=models.CASCADE)
    temporary_insurance = models.ForeignKey(TemporaryInsurance, db_column="verzekeringsid", on_delete=models.CASCADE)

    class Meta:
        db_table = "VRZKNIETLEDENTIJD"
        managed = False
