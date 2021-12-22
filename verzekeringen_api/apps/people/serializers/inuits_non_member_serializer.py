import logging

from rest_framework import serializers

from apps.people.models import InuitsNonMember, InuitsNonMemberTemplate

from scouts_auth.inuits.serializers import InuitsPersonSerializer
from scouts_auth.inuits.serializers.fields import OptionalCharField


logger = logging.getLogger(__name__)


class InuitsNonMemberSerializer(InuitsPersonSerializer, serializers.ModelSerializer):
    # id            pk

    # FIELDS INHERITED FROM InuitsPersonalDetails
    # first_name    max_length=15           required
    # last_name     max_length=25           required
    # phone_number  max_length=24           optional
    # cell_number   max_length=24           optional
    # email         EmailField              optional
    # birth_date    date                    optional
    # gender        choices=Gender.choices  optional

    # FIELDS INHERITED FROM InuitsAddress
    # street        max_length=100          optional
    # number        max_length=5            optional
    # letter_box    max_length=5            optional
    # postal_code   number                  optional
    # city          max_length=40           optional
    # country       InuitsCountry           optional

    # comment       max_length=500      optional
    class Meta:
        model = InuitsNonMember
        fields = "__all__"

    def to_internal_value(self, data):
        logger.debug("DATA: %s", data)

        group_admin_id = data.pop("group_group_admin_id", None)
        if group_admin_id:
            logger.warn("Discarding irrelevent group admin id for non-member")

        return data

    def to_representation(self, obj: InuitsNonMember = None) -> dict:
        # HACKETY HACK
        obj.id = InuitsNonMember.objects.all().filter(template__non_member=obj.id).first().id

        return super().to_representation(obj)

    def validate(self, data: dict) -> InuitsNonMember:
        return InuitsNonMember(
            id=data.get("id", None),
            first_name=data.get("first_name", None),
            last_name=data.get("last_name", None),
            phone_number=data.get("phone_number", None),
            cell_number=data.get("cell_number", None),
            email=data.get("email", None),
            birth_date=data.get("birth_date", None),
            gender=data.get("gender", None),
            street=data.get("street", None),
            number=data.get("number", None),
            letter_box=data.get("letter_box", None),
            postal_code=data.get("postal_code", None),
            city=data.get("city", None),
            comment=data.get("comment", None),
            company_name=data.get("company_name", None),
        )
