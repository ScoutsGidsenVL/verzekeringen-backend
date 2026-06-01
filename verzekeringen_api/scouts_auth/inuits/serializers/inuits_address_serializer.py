import logging, re

from rest_framework import serializers

from scouts_auth.inuits.models import InuitsAddress


logger = logging.getLogger(__name__)


class InuitsAddressSerializer(serializers.Serializer):
    # street        max_length=100          optional
    # number        max_length=5            optional
    # letter_box    max_length=5            optional
    # postal_code   number                  optional
    # city          max_length=40           optional
    # country       InuitsCountry           optional

    class Meta:
        model = InuitsAddress
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        postal_code = data.get("postal_code")
        if postal_code is not None and postal_code != "":
            # Buitenlandse postcodes kunnen letters bevatten (bv. "1234 AB" in Nederland).
            # We bewaren enkel de cijfers; het numerieke deel volstaat als benadering.
            # Bij een volledig niet-numerieke waarde vallen we terug op 0.
            digits_only = re.sub(r"\D", "", str(postal_code))
            data = data.copy()
            data["postal_code"] = int(digits_only) if digits_only else 0
        return super().to_internal_value(data)
