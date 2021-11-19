import logging

from groupadmin.models import (
    ScoutsMemberPersonalData,
    ScoutsMemberGroupAdminData,
    ScoutsMemberScoutsData,
    ScoutsMember,
    ScoutsAddress,
)
from groupadmin.serializers import (
    ScoutsLinkSerializer,
    ScoutsContactSerializer,
    ScoutsAddressSerializer,
    ScoutsFunctionSerializer,
    ScoutsGroupSerializer,
    ScoutsGroupSpecificFieldSerializer,
)

from inuits.models import GenderHelper
from inuits.serializers import NonModelSerializer


logger = logging.getLogger(__name__)


class ScoutsMemberPersonalDataSerializer(NonModelSerializer):
    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return None

        validated_data: dict = {"gender": data.pop("geslacht", None), "phone_number": data.pop("gsm", None)}

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    # def to_representation(self, instance: ScoutsMemberPersonalData) -> dict:
    #     return {
    #         "gender": str(instance.gender),
    #         "phone": instance.phone,
    #     }

    def save(self) -> ScoutsMemberPersonalData:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> ScoutsMemberPersonalData:
        if validated_data is None:
            return None

        instance = ScoutsMemberPersonalData()

        instance.gender = GenderHelper.parse_gender(validated_data.pop("gender", None))
        instance.phone_number = validated_data.pop("phone_number", None)

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance


class ScoutsMemberGroupAdminDataSerializer(NonModelSerializer):
    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return None

        validated_data: dict = {
            "first_name": data.pop("voornaam", None),
            "last_name": data.pop("achternaam", None),
            "birth_date": data.pop("geboortedatum", None),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    # def to_representation(self, instance: ScoutsMemberGroupAdminData) -> dict:
    #     return {
    #         "first_name": instance.first_name,
    #         "last_name": instance.last_name,
    #         "birth_date": instance.birth_date,
    #     }

    def save(self) -> ScoutsMemberGroupAdminData:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> ScoutsMemberGroupAdminData:
        if validated_data is None:
            return None

        instance = ScoutsMemberGroupAdminData()

        instance.first_name = validated_data.pop("first_name", None)
        instance.last_name = validated_data.pop("last_name", None)
        instance.birth_date = validated_data.pop("birth_date", None)

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance


class ScoutsMemberScoutsDataSerializer(NonModelSerializer):
    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return None

        validated_data: dict = {
            "membership_number": data.pop("lidnummer", None),
            "customer_number": data.pop("klantnummer", None),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> ScoutsMemberScoutsData:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> ScoutsMemberScoutsData:
        if validated_data is None:
            return None

        instance = ScoutsMemberScoutsData()

        instance.membership_number = validated_data.pop("membership_number", None)
        instance.customer_number = validated_data.pop("customer_number", None)

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance


class ScoutsMemberSerializer(NonModelSerializer):
    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return None

        validated_data: dict = {
            "personal_data": ScoutsMemberPersonalDataSerializer().to_internal_value(
                data.pop("persoonsgegevens", None)
            ),
            "group_admin_data": ScoutsMemberGroupAdminDataSerializer().to_internal_value(
                data.pop("vgagegevens", None)
            ),
            "scouts_data": ScoutsMemberScoutsDataSerializer().to_internal_value(data.pop("verbondsgegevens", None)),
            "email": data.pop("email", None),
            "username": data.pop("gebruikersnaam", None),
            "group_admin_id": data.pop("id", None),
            "addresses": ScoutsAddressSerializer(many=True).to_internal_value(data.pop("adressen", [])),
            "contacts": ScoutsContactSerializer(many=True).to_internal_value(data.pop("contacten", [])),
            "functions": ScoutsFunctionSerializer(many=True).to_internal_value(data.pop("functies", [])),
            "groups": ScoutsGroupSerializer(many=True).to_internal_value(data.pop("groups", [])),
            "group_specific_fields": ScoutsGroupSpecificFieldSerializer().to_internal_value(
                data.pop("groepseigenVelden", {})
            ),
            "links": ScoutsLinkSerializer(many=True).to_internal_value(data.pop("links", [])),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> ScoutsMember:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> ScoutsMember:
        if validated_data is None:
            return None

        instance = ScoutsMember()

        instance.personal_data = ScoutsMemberPersonalDataSerializer().create(validated_data.pop("personal_data", None))
        instance.group_admin_data = ScoutsMemberGroupAdminDataSerializer().create(
            validated_data.pop("group_admin_data", None)
        )
        instance.scouts_data = ScoutsMemberScoutsDataSerializer().create(validated_data.pop("scouts_data", None))
        instance.email = validated_data.pop("email", None)
        instance.username = validated_data.pop("username", None)
        instance.group_admin_id = validated_data.pop("group_admin_id", None)
        instance.addresses = ScoutsAddressSerializer(many=True).create(validated_data.pop("addresses", []))
        instance.contacts = ScoutsContactSerializer(many=True).create(validated_data.pop("contacts", []))
        instance.functions = ScoutsFunctionSerializer(many=True).create(validated_data.pop("functions", []))
        instance.groups = ScoutsGroupSerializer(many=True).create(validated_data.pop("groups", []))
        instance.group_specific_fields = ScoutsGroupSpecificFieldSerializer().create(
            validated_data.pop("group_specific_fields", {})
        )
        instance.links = ScoutsLinkSerializer(many=True).create(validated_data.pop("links", []))

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance


class ScoutsMemberSearchFrontendSerializer(NonModelSerializer):
    def to_representation(self, instance: ScoutsMember) -> dict:
        serialized = {}

        serialized["group_admin_id"] = instance.group_admin_id
        serialized["gender"] = instance.personal_data.gender
        serialized["email"] = instance.email
        serialized["phone_number"] = instance.personal_data.phone_number
        serialized["first_name"] = instance.group_admin_data.first_name
        serialized["last_name"] = instance.group_admin_data.last_name
        serialized["birth_date"] = instance.group_admin_data.birth_date
        serialized["membership_number"] = instance.scouts_data.membership_number
        serialized["customer_number"] = instance.scouts_data.customer_number

        if instance.addresses and len(instance.addresses) > 0:
            address: ScoutsAddress = instance.addresses[0]
            serialized["street"] = address.street
            serialized["number"] = address.number
            serialized["letter_box"] = address.letter_box
            serialized["postcode_city"] = {
                "city": address.city,
                "postcode": address.postal_code,
            }
        else:
            serialized["street"] = None
            serialized["number"] = None
            serialized["letter_box"] = None
            serialized["postcode_city"] = None
        # @TODO this should not be here
        serialized["is_member"] = True

        return serialized


class ScoutsMemberFrontendSerializer(NonModelSerializer):
    def to_representation(self, instance: ScoutsMember) -> dict:
        serialized: dict = super().to_representation(instance)

        serialized["group_admin_id"] = instance.group_admin_id
        serialized["gender"] = instance.personal_data.gender
        serialized["email"] = instance.email
        serialized["phone_number"] = instance.personal_data.phone_number
        serialized["first_name"] = instance.group_admin_data.first_name
        serialized["last_name"] = instance.group_admin_data.last_name
        serialized["birth_date"] = instance.group_admin_data.birth_date
        serialized["membership_number"] = instance.scouts_data.membership_number
        serialized["customer_number"] = instance.scouts_data.customer_number

        if instance.addresses and len(instance.addresses) > 0:
            address: ScoutsAddress = instance.addresses[0]
            serialized["street"] = address.street
            serialized["number"] = address.number
            serialized["letter_box"] = address.letter_box
            serialized["postcode_city"] = {
                "city": address.city,
                "postcode": address.postal_code,
            }
        # @TODO this should not be here
        serialized["is_member"] = True

        return serialized
