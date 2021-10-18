from rest_framework import serializers

from apps.locations.models import Country


class CountryOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("id", "name")
