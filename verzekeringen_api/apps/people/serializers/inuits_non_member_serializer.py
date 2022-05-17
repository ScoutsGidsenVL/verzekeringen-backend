import logging, uuid

from rest_framework import serializers

from apps.people.models import InuitsNonMember

from scouts_auth.inuits.models.enums import Gender
from scouts_auth.inuits.serializers import InuitsPersonSerializer
from scouts_auth.inuits.serializers.fields import OptionalCharField


logger = logging.getLogger(__name__)


class InuitsNonMemberSerializer(InuitsPersonSerializer, serializers.ModelSerializer):
    # id                pk

    # FIELDS INHERITED FROM InuitsPersonalDetails
    # first_name        max_length=15           required
    # last_name         max_length=25           required
    # phone_number      max_length=24             optional
    # cell_number       max_length=24           optional
    # email             EmailField              optional
    # birth_date        date                    optional
    # gender            choices=Gender.choices  optional

    # FIELDS INHERITED FROM InuitsAddress
    # street            max_length=100          optional
    # number            max_length=5            optional
    # letter_box        max_length=5            optional
    # postal_code       number                  optional
    # city              max_length=40           optional
    # country           InuitsCountry           optional

    # comment           max_length=500          optional
    # group_admin_id                            optional
    # company_name                              optional
    class Meta:
        model = InuitsNonMember
        fields = "__all__"

    def to_internal_value(self, data):
        logger.debug("INUITS NON MEMBER DESERIALIZER DATA: %s", data)
        id = data.get("id")

        # This is removed because actual members can be added as InuitsNonMembers for some insurances
        #
        # group_admin_id = data.pop("group_group_admin_id", None)
        # if group_admin_id:
        #     logger.warn("Discarding irrelevent group admin id for non-member")

        data = super().to_internal_value(data)

        data["id"] = id

        return data

    def to_representation(self, obj: InuitsNonMember = None) -> dict:
        logger.debug("HERE: %s", obj)
        # HACKETY HACK
        inuits_non_member = InuitsNonMember.objects.all().filter(template__non_member=obj.id).last()

        if inuits_non_member:
            obj.id = inuits_non_member.id

        return super().to_representation(obj)

    def validate(self, data: any) -> InuitsNonMember:
        logger.debug("DATA: %s", data)
        return InuitsNonMember(
            id=data.get("id", None),
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            phone_number=data.get("phone_number", ""),
            cell_number=data.get("cell_number", ""),
            email=data.get("email", ""),
            birth_date=data.get("birth_date", None),
            gender=data.get("gender", Gender.UNKNOWN),
            street=data.get("street", ""),
            number=data.get("number", ""),
            letter_box=data.get("letter_box", ""),
            postal_code=data.get("postal_code", ""),
            city=data.get("city", ""),
            comment=data.get("comment", ""),
            # group_admin_id=data.get("group_admin_id", ""),
            company_name=data.get("company_name", ""),
            created_by=data.get("created_by", None),
        )
