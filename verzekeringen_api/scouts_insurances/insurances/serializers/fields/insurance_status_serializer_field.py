from rest_framework import serializers

from scouts_insurances.insurances.models.enums import InsuranceStatus


class InsuranceStatusSerializerField(serializers.ChoiceField):
    pass
